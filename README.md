
# Echo Social Network

A fully functional Twitter-like social networking application built on the Python-based Django framework. Complete with an infinite-scrolling post feed, replies, reposts, follows, private messages, detailed user profiles, an auto-updating news feed, and search functionality to browse the users and content contained in Echo's database.


## Features

- Posts, replies and reposts with infinite-scrolling feed
- Followers/following functionality with dedicated follows post feed
- Detailed user profiles with browsable posts, replies and likes tabs
- User avatar upload with in-browser image manipulation
- Private messaging with traversable, time-stamped message history
- Current news feeds for tech, entertainment and world news
- User, post and news article search functionality
- Optimized for both desktop and mobile users
- Public API access to display content through 3rd parties
- Offers OIDC single sign-on provider functionality

## Optimizations

Uploaded avatar images are deconstructed with BytesIO and repackaged as 300x300 RGBA WebP format image files to optimize for bandwidth and storage capacity, as well as filename normalization.

Custom password hashing, security tokens and both server and client-side authentication measures to ensure data integrity and server security.

Recursive model relationship between private message and chat instance models, mimicking SQL associative entities, in order to reduce number of redundant, pre-filtered objects returned in querysets and reduce server load.

Temporary client-side storage of user session authentication data to reduce number of rejected server requests by allowing client to pre-emptively handle the majority of request validation.

## Roadmap

- Split into single page application and REST API
- Migrate to ASGI

## Tech Stack

**Client:** HTML, CSS, jQuery

**Server:** Python, Django, PostgreSQL

## License

[MIT](https://choosealicense.com/licenses/mit/)

