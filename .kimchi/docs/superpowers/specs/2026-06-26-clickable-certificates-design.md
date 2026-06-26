# Clickable Certificates & Projects with Image Previews

## Goal
Make the certificates and projects sections interactive: each certificate card and each project screenshot should be clickable and show the larger image in an on-page modal/lightbox. Certificate cards display a preview thumbnail at the top; project cards display a screenshot gallery.

## Current State
- `index.html` contains a `.certs-grid` with 6 `.cert-card` elements.
- Cards display name, issuer/date, and a short note only.
- `profile.json` has a `certifications` array with an empty `certificate_url` field per entry, and a `projects` array with an empty `images` array per entry.
- `generate_static.py` renders `profile.json` into `index.html`.
- `static/css/style.css` styles `.cert-card` and `.project-images` but does not support modal previews.

## Design

### 1. Image Storage
Certificate and project images/PDFs must be added to the repository so they are accessible when the site is deployed.

- **Certificates:** `static/images/certs/`
  - `google-cloud-pcse.jpg`
  - `cloud-computing-security.jpg`
  - `on-demand-it-skills.jpg`
  - `devops-micro-internship.jpg`
  - `build-ai-agents-for-business.jpg`
  - `agentic-ai-devops-automation.jpg`
- **Projects:** `static/images/projects/`
  - One folder or set of filenames per project, e.g.:
    - `spring-petclinic-1.jpg`, `spring-petclinic-2.jpg`, ...
    - `kubernetes-lab-1.jpg`, `kubernetes-lab-2.jpg`, ...
    - `epicbook-azure-1.jpg`, `epicbook-azure-2.jpg`, ...

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
- If `image` is empty, the card will not be clickable until an image is provided.

Extend each project entry with an `images` array:

```json
{
  "name": "Spring PetClinic Microservices",
  "images": [
    "static/images/projects/spring-petclinic-1.jpg",
    "static/images/projects/spring-petclinic-2.jpg"
  ]
}
```

### 3. Generator Update (`generate_static.py`)
Update `cert_card()` to:

1. Render an optional `<img>` thumbnail at the top of the card.
2. Render the `.cert-card` as a `<div>` with a `data-image` attribute when an image is present.
3. Add a `.cert-card-clickable` class to indicate the card is interactive.
4. Keep existing border and date color logic.
5. Use a placeholder visual when no image is provided (a styled badge/icon area so the layout does not collapse).

Add a `project_images_html()` helper and update the project card template to:

1. Render a `.project-images` grid when a project has images.
2. Each screenshot is an `<img class="project-image">`.

Add a hidden modal element at the bottom of the page for displaying the full image.

HTML structure for clickable certificate cards:

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

HTML structure for unlinked certificate cards (no image yet):

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

HTML structure for project screenshot gallery:

```html
<div class="project-images">
  <img src="static/images/projects/..." alt="Project Name screenshot 1" class="project-image" loading="lazy">
  <img src="static/images/projects/..." alt="Project Name screenshot 2" class="project-image" loading="lazy">
</div>
```

Modal element:

```html
<div id="certModal" class="cert-modal" aria-hidden="true">
  <div class="cert-modal-backdrop"></div>
  <div class="cert-modal-content">
    <button class="cert-modal-close" aria-label="Close image preview">&times;</button>
    <img id="certModalImg" src="" alt="Image preview">
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
Add a generic image modal behavior:

1. Select modal elements (`#certModal`, `#certModalImg`, close button, backdrop).
2. Attach click listeners to `.cert-card-clickable` cards to open the modal with the image from `data-image`.
3. Attach click listeners to `.project-image` screenshots to open the modal with the clicked image.
4. Close the modal when clicking the close button, clicking the backdrop, or pressing Escape.
5. Prevent body scroll when the modal is open.
6. Ignore clicks when the user is selecting text.

### 6. Responsive Behavior
- The existing `.certs-grid` is 3 columns on desktop, 2 on tablet, 1 on mobile.
- Thumbnails will scale with the card width and maintain the 16:10 ratio.
- Modal uses reduced padding on small screens and keeps the image within viewport bounds.

## Success Criteria
- [ ] Each certificate card with an image path is clickable.
- [ ] Each project screenshot is clickable.
- [ ] Clicking opens the image in an on-page modal/lightbox.
- [ ] Each certificate card has a preview thumbnail area at the top.
- [ ] Each project with images shows a screenshot gallery.
- [ ] Cards/images without a provided file show a placeholder instead of a broken image.
- [ ] The modal closes via close button, backdrop click, or Escape key.
- [ ] The site regenerates from `profile.json` without losing the changes.
- [ ] No new external dependencies are introduced.

## Open Questions / Next Steps for User
1. Copy certificate image/PDF files into `static/images/certs/`.
2. Copy project screenshot files into `static/images/projects/`.
3. Update the `image`/`certificate_url` fields in `profile.json` with the actual certificate filenames.
4. Update the `images` arrays in `profile.json` with the actual project screenshot filenames.
5. Re-run `generate_static.py` after adding images.
