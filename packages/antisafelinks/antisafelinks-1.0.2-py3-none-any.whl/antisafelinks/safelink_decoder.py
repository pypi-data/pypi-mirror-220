#! /usr/bin/env python3
import sys
import argparse
import mailbox
import email
import urllib
from pathlib import Path
from functools import partial
from concurrent.futures import ProcessPoolExecutor


def recover_link(url: str, debug=False):
    """Recovers the original url included in "url", when  is a M$cro$oft SafeLink url
    that perverted (and most of the times corrupted) the original link.
    If the introduced url is not a M$cro$oft SafeLink, it will return the same (unmodified) string.
    """
    if debug:
        print(f"Recover_link from {url}")

    if 'safelinks.protection.outlook' in url:
        if url.find("&amp;data=05") != -1:
            url = url[url.find("?url="):url.find("&amp;data=05")].lstrip("?url=")
        else:
            url = url[url.find("?url="):url.find("&data=05")].lstrip("?url=")

        if debug:
            print(f"and now:\n{urllib.parse.unquote(url).strip()}")

        return urllib.parse.unquote(url).strip()

    if debug:
        print("Safelinks not found in the previous link.")

    return url


def recover_links_in_text(text: str, debug=False):
    """Recovers all links that are present in the given text.
    It returns the recovered text.
    """
    mod_text = str(text)
    seed_start = 'https://eur03.safelinks.protection.outlook'
    seed_end1, seed_end2 = '&reserved=0', '&amp;reserved=0'
    while has_safelinks(mod_text):
        # if debug:
        #     print(f"Safelink found in {mod_text}.")
        pos0 = mod_text.find(seed_start)
        if (seed_end1 not in mod_text[pos0:]) and (seed_end2 not in mod_text[pos0:]):
            break

        pos1 = mod_text[pos0:].find(seed_end1)
        pos2 = mod_text[pos0:].find(seed_end2)

        if (pos1 == -1) and (pos2 == -1):
            print("Broken link in the email")
            break
        elif (pos1 != -1) and (pos2 != -1):
            seed_end = seed_end1 if pos1 < pos2 else seed_end2
        elif pos1 != -1:
            seed_end = seed_end1
        elif pos2 != -1:
            seed_end = seed_end2

        pos_end = pos0 + mod_text[pos0:].find(seed_end) + len(seed_end)
        url_recovered = recover_link(mod_text[pos0:pos_end], debug=debug)
        if debug:
            print(f"Recovered url in {url_recovered}\n from {mod_text[pos0:pos_end]}.")

        # The text should be clear of shit safelinks
        if has_safelinks(url_recovered):
            print("Broken link in the email")
            break

        mod_text = mod_text[:pos0] + url_recovered + mod_text[pos_end:]

    return mod_text


def has_safelinks(text: str, debug=False):
    """Given a text, it checks if it contains url fucked up by M$cro$oft SafeLinks.
    Retuns a boolean with the result.
    """
    return 'https://eur03.safelinks.protection.outlook' in text


def recover_email(message: mailbox.MaildirMessage, debug=False):
    """Given a file that should contain an RFC 2822-compliant message, it will modify back
    all links, if existing, in the body.
    """
    for part in message.walk():
        # charset = part.get_charsets()
        if part.get_content_maintype() == 'multipart':
            # multipart are just containers
            continue
        elif (part.get_content_maintype() == 'text') and \
             ('attachment' not in str(part.get('Content-Disposition'))):
            try:
                email_body = part.get_payload(decode=True).decode()
                if not has_safelinks(email_body):
                    continue

                print(f"Safelinks found in {message['Message-ID']}")
                part.set_payload(recover_links_in_text(email_body, debug=debug).encode())
            except UnicodeDecodeError as e:
                print(f"UnicodeDecodeError on email {message['Message-ID']}: {e}")
                return None

    return message


def this_is_a_test():
    print("TEST")

def recover_email_from_file(email_file: str, outfile: str = None, debug=False):
    """Given a file that should contain an RFC 2822-compliant message, it will modify back
    all links, if existing, in the body.
    """
    e = email.message_from_file(open(email_file, 'r'))

    if (new_e := recover_email(e, debug=debug)) is None:
        return

    if outfile is None:
        with open(email_file, 'w') as outemail:
            print(f"Overwriting {email_file}...")
            gen = email.generator.Generator(outemail, policy=e.policy)
            gen.flatten(new_e)

    else:
        with open(outfile, 'w') as outemail:
            print(f"Creating {outfile}...")
            gen = email.generator.Generator(outemail, policy=e.policy)
            gen.flatten(new_e)

    del e, new_e


def recover_maildir(maildir: str, check='all', debug=False):
    """Given a Maildir directory, it will go through all found email files and correct
    the links in there.

    Inputs
    maildir : str
        Maildir directory.
    check : str ('new', 'cur', 'tmp', or 'all')
        To only check the messages from the given folder.
        If 'all', all folders (new/cur/tmp) will be checked.
    """
    assert check in ('tmp', 'new', 'cur', 'all'), \
        f"The check parameter should be either 'tmp', 'cur', 'new', or 'all', but is '{check}'."

    box = mailbox.Maildir(maildir, create=False)
    try:
        box.lock()
        for key in box.iterkeys():
            try:
                message = box.get_message(key)
            except KeyError as e:
                print(f"{e}: Message with key {key} not found.")
                continue

            if (check == 'all') or (message.get_subdir() == check):
                print(f"Parsing message {key}")
                if (mod_message := recover_email(message)) is not None:
                    try:
                        box.update({key: mod_message})
                        print(f"Updated email {key}")
                    except UnicodeEncodeError:
                        # TODO: fix this, first move the payload functions to a non-legacy code.
                        print(f"UnicodeError for message {key}")
                        return None
                    finally:
                        del message
                        del mod_message
                else:
                    del message
                    del mod_message
    finally:
        box.flush()
        box.unlock()
        del box


def main():
    """Runs the main AntiSafeLinks program as CLI.
    """
    description = """Recovers the original url links that have been modified by
    the shit Microsoft SafeLink tool.
    """
    usage = "$(prog)s  [-h]  [-u/--url SafeLink-modified URL] " \
            " [-e/--email email_file]  [-m/--maildir Maildir folder]"
    parser = argparse.ArgumentParser(description=description, prog='safelink_decoder.py',
                                     usage=usage)
    parser.add_argument('-u', '--url', default=None, type=str,
                        help="URL fucked up by Microsoft that needs to be recovered. " \
                             "The output will be printed in STDOUT unless -o/--output is set.")
    parser.add_argument('-e', '--email', default=None, type=str,
                        help="Local email file to be parsed.")
    parser.add_argument('-m', '--maildir', default=None, type=str,
                        help="Local Maildir folder to be parsed.")
    parser.add_argument('-d', '--dir', default=None, type=str,
                        help="Local folder including Maildir folders to be parsed.")
    parser.add_argument('-o', '--output', default=None, type=str,
                        help="If file (-e/--email) used, instead " \
                        "of in-file replacing, it will generate this output file.")
    parser.add_argument('-n', '--only-new', default=False, action="store_true",
                        help="If given, it will only scan emails in the 'new' directory. " \
                             "Otherwise it will scan all new/cur/tmp folders.")
    parser.add_argument('--debug', default=False, action="store_true", help="More verbose output.")

    args = parser.parse_args()

    if (args.url, args.email, args.maildir, args.dir).count(None) != 3:
        print("One and only one of the following options need to be set:")
        print(" -e/--email - pointing to an existing file that may or may not contain " \
              "M$croso$t fucked-up links.")
        print(" -m/--maildir- pointing to an existing Maildir folder whose emails need to " \
              "be corrected from M$croso$t fucked up links.")
        print(" -d/--dir- pointing to an existing folder incluidng Maildir subfolders whose " \
              "emails need to be corrected from M$croso$t fucked up links.")
        print(" -u/--url - passing a url that has been fucked up by M$croso$t SafeLink tool.")
        print("Run me with -h for more help.")
        sys.exit(0)

    if args.url is not None:
        print(recover_link(args.url))
    elif args.dir is not None:
        main_dir = Path(args.dir)
        if main_dir.exists():
            print(f"Parsing directory {main_dir}")
            with ProcessPoolExecutor(max_workers=4) as executor:
                executor.map(partial(recover_maildir, check='new' if args.only_new else 'all'),
                             main_dir.iterdir())
        else:
            print(f"The directory {args.dir} could not be found.")
    elif args.maildir is not None:
        if Path(args.maildir).exists():
            recover_maildir(args.maildir, debug=args.debug)
        else:
            print(f"The maildir directory {args.maildir} could not be found.")
    elif args.email is not None:
        if Path(args.email).exists():
            recover_email_from_file(args.email, args.output, debug=args.debug)
        else:
            print(f"The email {args.email} cannot be found.")


if __name__ == '__main__':
    main()
