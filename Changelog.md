## V1.7.37 (2020-11-25)

- Pre-built user colors + custom colors.
- Fixed media info bottom gap too big.
- Fixed "keyboard" buttons top gap too small.
- Messages content padding reduced.

## V1.6.36 (2020-11-20)

- A small patch for last fix ([Issue #12](../../issues/12)) to include other browsers like Chrome.

## V1.6.35 (2020-11-20)

- Fixed an issue that can occur when not using English as the UI language that causes the send button to get bigger and pushes other buttons down. [Issue #12](../../issues/12)

## V1.6.34 (2020-11-18)

- This update contains fixes towards [Issue #12](../../issues/12) to take into account answering buttons in some channels.
- Added bot channels header & intro message.
- Added new reply buttons style to the composer textarea.

## V1.5.33 (2020-10-09)

- Added the 'Pose mode' that was hidden in the style as a feature you can enable. Can't see how you will use this toy.. but it can be handy maybe as a separated more private mode. Also this feature drew dome big changes in the style. Please report any issues as usual :) .
- Fixed service message for pinned messages vertical align.
- Messages date & time no longer unnecessarily highlighted.

## V1.4.32 (2020-10-07)

- Fixed scroll bars thumb leaking when mouse isn't around.

## V1.4.31 (2020-10-07)

- Fixed focused elements outline to math the theme's colors.

## V1.4.30 (2020-10-07)

- Separated preview messages width for incoming or outgoing messages.
- Added preview messages height.

## V1.3.30 (2020-10-07)

- Added messages text align.
- You can now set the preview size of photo and video thumbnails. (set within reason with chat bubbles width.)
- Video thumbs info got fancier.
- Fixed wrong video info position in some situations.
- Fixed pause SVG file to load from the file rather that fetching it every time from GitHub.

## V1.2.29 (2020-10-05)

- Versioning updated please review [Issue #11](../../issues/11).
- Fixed overflow of audio message box.
- Fixed unread (or unheard) audio message indicator.
- Fixed redundant background color from mentions.
- Fixed mention drop down list items colors.
- Added more tail options.
- You can now center authors name within their bubbles. good when you're not using any tail and a big round borders. try it :)

## V1.1.28 (2020-10-02)

- Added a zoom effect when focusing on popups and media.

## V1.1.27 (2020-10-01)

- Added blur behind.
- Added window width.
- Added a switch to fix the conversation list width issue on some browsers like FireFox. (Yes.. 🙄 a manual fix is required here for now as there's no way to detect browser that I know of.)

## V1.1.26 (2020-09-30)

- Fixed messages tail visible seam in some zoom levels.
- Fixed inconsistent messages content.
- Fixed vote buttons and added a bg to them.
- Fixed pinned message.
- Removed ugly border from reply messages.
- Added a maximum width for messages bubbles. (Set to 100% to ignore maximum width.)
- Empty conversation now also have a fancy banner.
- Fixed send buttons area mess when zooming to much in.
- (~~May~~ Did 😎) Fixed the conversation list width issue on some browsers.

## V1.1.25 (2020-09-15)

- Fixed pinned messages hide button not showing the custom dedicated svg icon.

## V1.1.24 (2020-09-15)

- Fixed an issue with pinned messages were the side ribbon taking up the whole space.

## V1.1.23 (2020-09-15)

- Added a QR Code linking to the issues page on GitHub for lazy people like me who don't wanna manually write the link.

## V1.1.22 (2020-08-15)

- Fixed wrapping of long words. ([Issue #10](../../issues/10))

## V1.1.21 (2020-07-12)

- Changed the bottom most background to a darker control color.
- Bubbles will now only highlight in selection mode.
- On compact mode the header is now fixed.

## V1.1.20 (2020-06-18)

- Replaced hover & selected messages mechanics. Now the chat bubbles will highlight when hovered or selected.

## V1.1.19 (2020-04-28)

- Fixed media message audio button won't show up as a pause button when playing audio files.

## V1.1.18 (2020-04-28)

- Fixed media buttons background won't show up on Chromium based browsers.

## V1.1.17 (2020-04-28)

- Fixed file upload\download info won't show on Chromium based browsers. ([Issue #8](../../issues/8))

## V1.1.16 (2020-04-24)

- Fixed top padding of clickable media messages (non-animated stickers).
- Fixed width of video thumbnails.
- Fixed pinned message right margin.
- Fixed author name position.

## V1.1.15 (2020-04-16)

- New compile script to handle sync of styl and css file versions and make a darkmode.css Franz/Ferdi compatible plain css file based on the synced files.
- A few changes in code to follow the new script guidance.

## V1.0.14 (2020-04-10)

- Fixed login screen colors.

## V1.0.13 (2020-04-10)

- Renamed styl file to user.style to make stylus recognize it and be able to be installed. ([Issue #1](../../issues/1))
- Fixed the circular progress bar when loading messages.
- Fixed extra unneeded indentation for RTL input languages.

## V1.0.12 (2020-04-08)

- Added transition to emoji's and stickers.

## V1.0.11 (2020-04-08)

- Emoji's and stickers are now enlarged when hovered.

## V1.0.10 (2020-04-08)

- Fixed other mask issues. I'm so tired....

## V1.0.9 (2020-04-08)

- Fixed mask-image to include -webkit- -o- and -moz- that I forgot to include last version...

## V1.0.8 (2020-04-08)

- Added a noise texture to controls. may be expanded in the future.
- Replaced almost all bitmap icons with handmade SVG's.
- Fixed bg color leak when choosing to blur the background.

## V1.0.7 (2020-04-05)

- Added custom font.
- Fixed short incoming messages indentation when setting its bubble to right position.
- Fixed an issue with custom contact icons appearing behind contact icons.
- Fixed right tail position.
- A LOT of color tweaks.

## V1.0.6 (2020-04-05)

- Added bubble position.
- Added hiding contacts icon from chat.

## V1.0.5 (2020-04-04)

- Added fullscreen mode.
- Added an option to set chat width.
- Added Emojis and Stickers opacity.
- Fixed video thumbnail size to 256x256px.
- Fixed overflow background buttons with big border radius size.
- Fixed message body width to fit inside chat box.
- Fixed bottom part of contact-icon.

## V1.0.4 (2020-04-03)

- Compact mode ported from WhatsApp style.
  - There's an issue with the header, will be fixed in the future.
- Media and system messages now has a fancy background too.
- Shifted user photos a bit up.
- Drop area now animated with accent colors.
- You can now choose Emoji popup position.

## V1.0.3 (2020-04-02)

- A wild changelog appeared!
- Color filters to contact icon and name.
- Tails now uses selected bubbles color.
- Menus drop shadow fix.
- Bubble tails position fix.
