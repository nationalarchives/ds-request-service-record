# Request a military service record documentation

This documentation explains how the service is structured and how the key application patterns work.

## Key topics

- **State machine** — how the request journey is controlled and how the next page is chosen
- **Post-Redirect-Get** — how the service handles form submissions and redirects after POST requests
- **Content approach** — how page content, labels, and validation messages are stored and loaded
- **Hyperlinks** — how named link constants and markdown parsing are used to render outbound links consistently
- **Template approach** — why we keep templates simple and accept deliberate similarity where that makes the behaviour easier to reason about
- **Back links** — how the service decides where the Back link should go based on the user's journey
- **Testing** — how we cover browser journeys with Playwright and protect content usage and navigation behaviour with targeted tests

## Start here

- `core-patterns/state-machine.md`
- `core-patterns/post-redirect-get.md`
- `core-patterns/content-approach.md`
- `core-patterns/hyperlinks.md`
- `core-patterns/template-approach.md`
- `core-patterns/back-links.md`
- `testing/index.md`
