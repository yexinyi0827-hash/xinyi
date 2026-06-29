const workGrid = document.querySelector(".work-grid");
const filters = document.querySelectorAll(".filter");
const modal = document.querySelector(".modal");
const modalImage = modal.querySelector("img");
const modalCaption = modal.querySelector("figcaption");
const modalClose = modal.querySelector(".modal-close");

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function renderProjects() {
  const items = window.portfolioItems || [];
  workGrid.innerHTML = items
    .map((item, index) => {
      const id = index === 0 ? ' id="ui"' : index === window.portfolioCounts.ui ? ' id="graphic"' : index === window.portfolioCounts.ui + window.portfolioCounts.graphic ? ' id="video"' : "";
      const feature = index === 0 || index === window.portfolioCounts.ui ? " feature" : "";
      return `
        <article class="project${feature}"${id} data-category="${escapeHtml(item.category)}">
          <button class="project-media" data-modal-src="${escapeHtml(item.src)}" data-modal-title="${escapeHtml(item.title)}">
            <img src="${escapeHtml(item.src)}" alt="${escapeHtml(item.title)}" loading="lazy" />
          </button>
          <div class="project-copy">
            <span>${escapeHtml(item.categoryLabel)} / ${escapeHtml(item.subtype)}</span>
            <h3>${escapeHtml(item.title)}</h3>
            <p>${escapeHtml(item.original)}</p>
          </div>
        </article>
      `;
    })
    .join("");
}

function applyAdaptiveMedia(media) {
  const image = media.querySelector("img");
  if (!image || !image.naturalWidth || !image.naturalHeight) return;

  const width = image.naturalWidth;
  const height = image.naturalHeight;
  const ratio = width / height;
  const isLongImage = height / width >= 2.2;

  media.classList.remove("fit-contain", "fit-cover", "long-preview");

  if (isLongImage) {
    media.style.setProperty("--media-ratio", "16 / 9");
    media.classList.add("long-preview");
    return;
  }

  const roundedRatio = Math.max(0.68, Math.min(2.35, ratio));
  media.style.setProperty("--media-ratio", `${roundedRatio.toFixed(3)} / 1`);
  media.classList.add(ratio < 0.9 ? "fit-contain" : "fit-cover");
}

function bindAdaptiveMedia() {
  document.querySelectorAll(".project-media").forEach((media) => {
    const image = media.querySelector("img");
    if (!image) return;

    if (image.complete) {
      applyAdaptiveMedia(media);
    } else {
      image.addEventListener("load", () => applyAdaptiveMedia(media), { once: true });
    }
  });
}

function bindFilters() {
  const projects = document.querySelectorAll(".project");

  filters.forEach((button) => {
    button.addEventListener("click", () => {
      const category = button.dataset.filter;

      filters.forEach((item) => item.classList.remove("is-active"));
      button.classList.add("is-active");

      projects.forEach((project) => {
        const shouldShow = category === "all" || project.dataset.category === category;
        project.classList.toggle("is-hidden", !shouldShow);
      });
    });
  });
}

function openModal(src, title) {
  modalImage.src = src;
  modalImage.alt = title;
  modalCaption.textContent = title;
  modal.classList.add("is-open");
  modal.setAttribute("aria-hidden", "false");
  document.body.style.overflow = "hidden";
}

function closeModal() {
  modal.classList.remove("is-open");
  modal.setAttribute("aria-hidden", "true");
  modalImage.src = "";
  document.body.style.overflow = "";
}

function bindModalTriggers() {
  document.querySelectorAll("[data-modal-src]").forEach((trigger) => {
    trigger.addEventListener("click", () => {
      openModal(trigger.dataset.modalSrc, trigger.dataset.modalTitle);
    });
  });
}

renderProjects();
bindAdaptiveMedia();
bindFilters();
bindModalTriggers();

modalClose.addEventListener("click", closeModal);

modal.addEventListener("click", (event) => {
  if (event.target === modal) {
    closeModal();
  }
});

window.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && modal.classList.contains("is-open")) {
    closeModal();
  }
});
