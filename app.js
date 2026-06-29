const filters = document.querySelectorAll(".filter");
const projects = document.querySelectorAll(".project");
const modal = document.querySelector(".modal");
const modalImage = modal.querySelector("img");
const modalCaption = modal.querySelector("figcaption");
const modalClose = modal.querySelector(".modal-close");
const modalTriggers = document.querySelectorAll("[data-modal-src]");
const mediaBlocks = document.querySelectorAll(".project-media");

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
    media.dataset.preview = "top-16-9";
    return;
  }

  const roundedRatio = Math.max(0.68, Math.min(2.35, ratio));
  media.style.setProperty("--media-ratio", `${roundedRatio.toFixed(3)} / 1`);
  media.classList.add(ratio < 0.9 ? "fit-contain" : "fit-cover");
}

mediaBlocks.forEach((media) => {
  const image = media.querySelector("img");
  if (!image) return;

  if (image.complete) {
    applyAdaptiveMedia(media);
  } else {
    image.addEventListener("load", () => applyAdaptiveMedia(media), { once: true });
  }
});

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

modalTriggers.forEach((trigger) => {
  trigger.addEventListener("click", () => {
    openModal(trigger.dataset.modalSrc, trigger.dataset.modalTitle);
  });
});

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
