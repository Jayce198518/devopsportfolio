# Clickable Certificates with Image Thumbnails

## Goal
Make the certificates section in the portfolio interactive: each certificate card should be clickable and show the larger certificate image in an on-page modal/lightbox, with a preview thumbnail displayed at the top of each card.

## Current State
- `index.html` contains a `.certs-grid` with 6 `.cert-card` elements.
- Cards display name, issuer/date, and a short note only.
- `profile.json` has a `certifications` array with an empty `certificate_url` field per entry.
- `generate_static.py` renders `profile.json` into `index.html`.
- `static/css/style.css` styles `.cert-card` but does not support images or link wrapping.

## Design

### 1. Image Storage
Certificate images/PDFs must be added to the repository so they are accessible when the site is deployed.

- **Location:** `static/images/certs/`
- **Naming convention:** lowercase, hyphenated filenames based on certificate name, e.g.:
  - `google-cloud-pcse.jpg`
  - `cloud-computing-security.jpg`
  - `on-demand-it-skills.jpg`
  - `devops-micro-internship.jpg`
  - `build-ai-agents-for-business.jpg`
  - `agentic-ai-devops-automation.jpg`

### 2. Data Model
Extend each certification entry in `profile.json`:

```json
{
  "name": "Google Cloud Certified — Professional Cloud Security Engineer",
  "issuer": "Google Cloud",
  "date": "2025",
  "note": "...",
  "certificate_url": "static/images/certs/google-cloud-pcse.jpg",
  "image": "static/images/certs/google-cloud-pcse.jpg"
}
```

- `certificate_url` / `image`: path to the certificate image or PDF.
- If `certificate_url` is empty, the card will not be wrapped in a link and will remain non-clickable until an image is provided.

### 3. Generator Update (`generate_static.py`)
Update `cert_card()` to:

1. Render an optional `<img>` thumbnail at the top of the card.
2. Render the `.cert-card` as a `<div>` with a `data-image` attribute when an image is present.
3. Add a `.cert-card-clickable` class to indicate the card is interactive.
4. Keep existing border and date color logic.
5. Use a placeholder visual when no image is provided (a styled badge/icon area so the layout does not collapse).
6. Add a hidden modal element at the bottom of the page for displaying the full certificate image.

HTML structure for clickable cards:

```html
<div class="cert-card cert-card-clickable" data-image="static/images/certs/..." style="...">
  <div class="cert-thumb">
    <img src="static/images/certs/..." alt="Certificate: Name" loading="lazy">
  </div>
  <div class="cert-name">...</div>
  <div class="cert-date">...</div>
  <div class="cert-note">...</div>
</div>
```

HTML structure for unlinked cards (no image yet):

```html
<div class="cert-card" style="...">
  <div class="cert-thumb cert-thumb-placeholder">
    <span>📜</span>
  </div>
  <div class="cert-name">...</div>
  <div class="cert-date">...</div>
  <div class="cert-note">...</div>
</div>
```

Modal element:

```html
<div id="certModal" class="cert-modal" aria-hidden="true">
  <div class="cert-modal-backdrop"></div>
  <div class="cert-modal-content">
    <button class="cert-modal-close" aria-label="Close certificate preview">&times;</button>
    <img id="certModalImg" src="" alt="Certificate preview">
  </div>
</div>
```

### 4. CSS Updates (`static/css/style.css`)
Add styles for:

- `.cert-card` as a flex column with inherited color.
- `.cert-card-clickable` with `cursor: pointer` to indicate interactivity.
- `.cert-thumb` container with fixed aspect ratio (e.g., 16:10), rounded corners, overflow hidden, and subtle border.
- `.cert-thumb img` with `width: 100%; height: 100%; object-fit: cover;`.
- `.cert-thumb-placeholder` with a muted background, centered icon, and same aspect ratio.
- Hover state for the clickable card: border color change plus a slight lift/shadow.
- Focus state for accessibility.
- Modal backdrop, content container, close button, and image sizing.
- Responsive modal padding for mobile.

Example CSS:

```css
.cert-card {
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: inherit;
}

.cert-card-clickable {
  cursor: pointer;
}

.cert-thumb {
  width: 100%;
  aspect-ratio: 16 / 10;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--border);
  margin-bottom: 0.5rem;
  background: var(--panel2);
}

.cert-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.25s ease, border-color 0.2s;
}

.cert-card:hover .cert-thumb img {
  transform: scale(1.03);
}

.cert-thumb-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  color: var(--ghost2);
}

.cert-modal {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.cert-modal.active {
  display: flex;
}
```

### 5. Regeneration
After updating `profile.json`, `generate_static.py`, and `style.css`, run:

```bash
python3 generate_static.py
```

This rebuilds `index.html` with the new certificate cards.

### 5. JavaScript Updates (`static/js/main.js`)
Add modal behavior:

1. Select modal elements (`#certModal`, `#certModalImg`, close button, backdrop).
2. Attach click listeners to `.cert-card-clickable` cards to open the modal with the image from `data-image`.
3. Close the modal when clicking the close button, clicking the backdrop, or pressing Escape.
4. Prevent body scroll when the modal is open.
5. Ignore clicks when the user is selecting text.

### 6. Responsive Behavior
- The existing `.certs-grid` is 3 columns on desktop, 2 on tablet, 1 on mobile.
- Thumbnails will scale with the card width and maintain the 16:10 ratio.
- Modal uses reduced padding on small screens and keeps the image within viewport bounds.

## Success Criteria
- [ ] Each certificate card with an image path is clickable.
- [ ] Clicking opens the certificate image in an on-page modal/lightbox.
- [ ] Each card has a preview thumbnail area at the top.
- [ ] Cards without an image show a placeholder instead of a broken image.
- [ ] The modal closes via close button, backdrop click, or Escape key.
- [ ] The site regenerates from `profile.json` without losing the changes.
- [ ] No new external dependencies are introduced.

## Open Questions / Next Steps for User
1. Copy certificate image/PDF files into `static/images/certs/`.
2. Update the `image`/`certificate_url` fields in `profile.json` with the actual filenames.
3. Re-run `generate_static.py` after adding images.
