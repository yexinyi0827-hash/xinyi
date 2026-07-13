const featuredGrid = document.querySelector(".featured-grid");
const uiShowcase = document.querySelector(".ui-showcase");
const graphicShowcase = document.querySelector(".graphic-showcase");
const videoGrid = document.querySelector(".video-grid");
const modal = document.querySelector(".modal");
const modalImage = modal.querySelector("img");
const modalVideo = modal.querySelector("video");
const modalCaption = modal.querySelector("figcaption");
const modalClose = modal.querySelector(".modal-close");

function escapeHtml(value) {
  return String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function projectButton(item, className = "work-media", extra = "") {
  return `
    <button class="${className}${item.video ? " has-video" : ""}${extra ? ` ${extra}` : ""}" data-modal-src="${escapeHtml(item.src)}" data-modal-title="${escapeHtml(item.title)}"${item.video ? ` data-modal-video="${escapeHtml(item.video)}"` : ""}>
      <img src="${escapeHtml(item.src)}" alt="${escapeHtml(item.title)}" loading="lazy" />
      ${item.video ? '<span class="play-badge">▶</span>' : ""}
    </button>
  `;
}

function projectMeta(item, label = item.subtype) {
  return `
    <div class="project-copy">
      <span>${escapeHtml(item.categoryLabel)} / ${escapeHtml(label)}</span>
      <h3>${escapeHtml(item.title)}</h3>
    </div>
  `;
}

function renderFeatured(items) {
  const featured = [
    items.find((item) => item.src.includes("14-graphic")),
    items.find((item) => item.src.includes("10-ui")),
    items.find((item) => item.src.includes("25-graphic")),
    items.find((item) => item.src.includes("01-ui")),
    items.find((item) => item.src.includes("40-video")),
  ].filter(Boolean);

  featuredGrid.innerHTML = featured
    .map((item, index) => {
      const sizeClass = index === 0 ? "is-lead" : index === 1 ? "is-wide" : "";
      return `
        <article class="feature-card ${sizeClass}">
          ${projectButton(item, "work-media", index === 0 ? "media-hero" : "")}
          ${projectMeta(item)}
        </article>
      `;
    })
    .join("");
}

function renderUi(uiItems) {
  const groups = [
    { title: "官网 Banner", note: "先用横向主视觉建立品牌气质。", items: uiItems.slice(0, 4), layout: "ui-banner-grid" },
    { title: "官网页面", note: "用完整页面展示信息组织和视觉延展。", items: uiItems.slice(4, 5), layout: "ui-page-grid" },
    { title: "产品页面", note: "突出 B 端产品界面的层级、卡片和操作信息。", items: uiItems.slice(5, 8), layout: "ui-product-grid" },
    { title: "数据看板", note: "宽屏展示更贴近真实业务场景。", items: uiItems.slice(8, 10), layout: "ui-dashboard-grid" },
  ];

  uiShowcase.innerHTML = groups
    .map((group) => `
      <section class="case-block">
        <div class="case-heading">
          <h3>${group.title}</h3>
          <p>${group.note}</p>
        </div>
        <div class="${group.layout}">
          ${group.items
            .map((item, index) => `
              <article class="case-card ${index === 0 ? "is-first" : ""}">
                ${projectButton(item, "work-media")}
                ${projectMeta(item, group.title)}
              </article>
            `)
            .join("")}
        </div>
      </section>
    `)
    .join("");
}

function renderGraphic(graphicItems) {
  const groups = [
    { title: "Banner / KV", note: "横向视觉优先放大，形成进入平面区的第一波冲击。", items: graphicItems.slice(0, 5), layout: "magazine-grid kv-grid" },
    { title: "印刷与展会", note: "海报、折页、展台和邀请函用错落图块体现物料丰富度。", items: graphicItems.slice(5, 18), layout: "magazine-grid event-grid" },
    { title: "运营与长图", note: "运营海报与长图页面分组展示，长图保留顶部 16:9 预览。", items: graphicItems.slice(18), layout: "magazine-grid long-grid" },
  ];

  graphicShowcase.innerHTML = groups
    .map((group) => `
      <section class="graphic-block">
        <div class="case-heading">
          <h3>${group.title}</h3>
          <p>${group.note}</p>
        </div>
        <div class="${group.layout}">
          ${group.items
            .map((item, index) => {
              const longClass = item.subtype.includes("闀") || item.original.includes("长图") || item.src.includes("35-graphic") || item.src.includes("36-graphic") || item.src.includes("37-graphic") || item.src.includes("38-graphic") || item.src.includes("39-graphic");
              const rhythm = index === 0 ? "is-large" : index % 5 === 2 ? "is-tall" : index % 6 === 4 ? "is-wide" : "";
              return `
                <article class="graphic-card ${rhythm}${longClass ? " is-long" : ""}">
                  ${projectButton(item, "work-media", longClass ? "long-preview" : "")}
                  ${projectMeta(item)}
                </article>
              `;
            })
            .join("")}
        </div>
      </section>
    `)
    .join("");
}

function renderVideos(videoItems) {
  videoGrid.innerHTML = videoItems
    .map((item) => `
      <article class="video-card">
        ${projectButton(item, "work-media video-media")}
        ${projectMeta(item)}
      </article>
    `)
    .join("");
}

function renderProjects() {
  const items = window.portfolioItems || [];
  renderFeatured(items);
  renderUi(items.filter((item) => item.category === "ui"));
  renderGraphic(items.filter((item) => item.category === "graphic"));
  renderVideos(items.filter((item) => item.category === "video"));
}

function applyAdaptiveMedia(media) {
  const image = media.querySelector("img");
  if (!image || !image.naturalWidth || !image.naturalHeight) return;

  const width = image.naturalWidth;
  const height = image.naturalHeight;
  const ratio = width / height;
  const isLongImage = height / width >= 2.2 || media.classList.contains("long-preview");

  media.classList.remove("fit-contain", "fit-cover", "long-preview-auto");

  if (isLongImage) {
    media.style.setProperty("--media-ratio", "16 / 9");
    media.classList.add("long-preview-auto");
    return;
  }

  const roundedRatio = Math.max(0.72, Math.min(2.45, ratio));
  media.style.setProperty("--media-ratio", `${roundedRatio.toFixed(3)} / 1`);
  media.classList.add(ratio < 0.92 ? "fit-contain" : "fit-cover");
}

function bindAdaptiveMedia() {
  document.querySelectorAll(".work-media").forEach((media) => {
    const image = media.querySelector("img");
    if (!image) return;

    if (image.complete) {
      applyAdaptiveMedia(media);
    } else {
      image.addEventListener("load", () => applyAdaptiveMedia(media), { once: true });
    }
  });
}

function openModal(src, title, videoSrc = "") {
  if (videoSrc) {
    modal.classList.add("is-video");
    modalVideo.src = videoSrc;
    modalImage.src = "";
    modalImage.alt = "";
    modalVideo.play().catch(() => {});
  } else {
    modal.classList.remove("is-video");
    modalImage.src = src;
    modalImage.alt = title;
    modalVideo.pause();
    modalVideo.removeAttribute("src");
    modalVideo.load();
  }
  modalCaption.textContent = title;
  modal.classList.add("is-open");
  modal.setAttribute("aria-hidden", "false");
  document.body.style.overflow = "hidden";
}

function closeModal() {
  modal.classList.remove("is-open");
  modal.classList.remove("is-video");
  modal.setAttribute("aria-hidden", "true");
  modalImage.src = "";
  modalVideo.pause();
  modalVideo.removeAttribute("src");
  modalVideo.load();
  document.body.style.overflow = "";
}

function bindModalTriggers() {
  document.querySelectorAll("[data-modal-src]").forEach((trigger) => {
    trigger.addEventListener("click", () => {
      openModal(trigger.dataset.modalSrc, trigger.dataset.modalTitle, trigger.dataset.modalVideo || "");
    });
  });
}

renderProjects();
bindAdaptiveMedia();
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
