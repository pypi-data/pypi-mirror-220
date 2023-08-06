# Microsoft Safelinks Annihilator


_Unleash the Real Links_


## Description

**AntiSafeLinks** is a liberating Python program that takes a stand against Microsoft's "security-driven" SafeLinks introduced in Office365 emails. This open-source tool empowers users to reclaim their original links by removing the suffocating "safelink" wrappers. If you are suffering Microsoft' actions and you want to 1) recover a particular url, 2) recover all the links from a email stored in a local file in your computer, or 3) you keep your mail box as a Maildir format locally, then you can use **AntiSafeLinks** to neutralize it.



### Why AntiSafeLinks?

Microsoft perverts the structure of your emails and, in fact, makes them more insecure by obscuring URL in your emails. These actions typically break multiple URLs that can lie in your email, avoids you to check before entering a URL what is the address it will take you to and, furthermore, Microsoft collects all metadata from you when accessing the SafeLinks website.

This tool has been created with the purpose of recovering all these emails when you actually do not have any other alternative because your company's sysadmins decisions.


### Features

- **Link Liberation**: AntiSafeLinks does one thing, and it does it well: it liberates your links from the "safelink" tyranny, restoring them to their true form.
- **Ease of Use**: Simply pass the program a modified URL, an email file, or a Maildir directory, and watch it go to work, effortlessly recovering all original links. You can put it as a cronjob and it will go through all your mail periodically.
- **Preserves Privacy**: No need to worry about your sensitive data being unnecessarily routed through Microsoft's servers. AntiSafeLinks ensures your privacy remains intact and only runs locally. Additionally, AntiSafeLinks does not require any external (Python) dependency to run.



## How To Use

1. **Modified URL**. Do you have a modified URL that you want to recover?

```bash
antisafelinks --url "URL-perverted-by-microsoft"
```

2. **Email file**. If you have an email stored locally in your computer as a single file that may contain SafeLinks URLs.

```bash
antisafelinks --email <PATH-TO-EMAIL-FILE>
```
Note that if you want to create a copy of the email, instead of modifying it in-situ, you can add the `--output <NEW-FILE>` option.

3. **Maildir directory**: If you keep your mail account as a Maildir directory locally in your computer, you can make AntiSafeLinks to run through the mailbox periodically (e.g. with a cronjob) calling it as:
```bash
antisafelinks --dir <PATH-TO-FOLDER-CONTAINING THE MAILDIR DIRECTORIES>
```

**As an example**, I personally synchronize (two-ways) my mail with [OfflineIMAP](https://www.offlineimap.org/) and [DavMail](https://davmail.sourceforge.net). Then I have a `cronjob` that runs AntiSafeLinks after retrieving new emails. Therefore, when it is synchronized again, all emails have been recovered to their original URL versions, and as such they show up in my Mailboxes.



## Installation


### Install it via Pip

```bash
pip install antisafelinks
```
or
```bash
python3 -m pip install antisafelinks
```


## Install from Source Code

1. Clone this repository to your preferred directory.
   `git clone https://github.com/bmarcote/antisafelinks.git`
2. Navigate to the `antisafelinks` directory.
3. Install the package with `python3 -m pip install .`


### Disclaimer

This tool is provided as-is and comes with no warranties or guarantees. Use it responsibly and at your own risk. We are not affiliated with Microsoft in any way, and this project is purely for personal joy.


### Contributing

We welcome contributions from fellow link liberators! If you believe in the cause and want to make AntiSafeLink even better, feel free to submit a pull request or open an issue.

### License

AntiSafeLink is released under the GPLv3 License, which is a permissive license allowing you to do whatever you damn well please with this code.


### Support Me with a Coffee!

If you find this software useful and you plan to use it in your day-to-day life, I'd like to extend an invitation to show your appreciation by ["paying me a coffee" donation](https://buymeacoffee.com/bmarcote). Every cup of coffee represents not just a token of gratitude but a gesture that helps me continue dedicating time and effort to enhance and maintain the software for all of you. Your support goes a long way in keeping this project alive and ensures that I can keep delivering top-notch features and improvements. So, if you find value in what I've crafted, consider contributing the cost of a coffee and be a vital part of our thriving community. Your generosity is greatly appreciated! ☕❤️
