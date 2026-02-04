/* =================================================
   BASE JS – LMS (Mobile + Desktop)
   Author: Banavath Mahendher
================================================= */

document.addEventListener("DOMContentLoaded", () => {

  /* ===============================
     NOTIFICATION CLICK
  =============================== */
  const notification = document.querySelector(".notification");
  const badge = document.querySelector(".badge");

  if (notification) {
    notification.addEventListener("click", () => {
      alert("🔔 You have new notifications!");
      if (badge) {
        badge.style.display = "none"; // hide badge after click
      }
    });
  }

  /* ===============================
     BUTTON HOVER EFFECT (DESKTOP)
  =============================== */
  document.querySelectorAll(".btn").forEach(btn => {
    btn.addEventListener("mouseenter", () => {
      btn.style.transform = "scale(1.05)";
    });
    btn.addEventListener("mouseleave", () => {
      btn.style.transform = "scale(1)";
    });
  });

  /* ===============================
     RESPONSIVE HERO IMAGE HEIGHT
  =============================== */
  function adjustHeroImage() {
    const heroImg = document.querySelector(".hero-img img");
    if (!heroImg) return;

    if (window.innerWidth <= 640) {
      heroImg.style.height = "220px";
    } else if (window.innerWidth <= 1024) {
      heroImg.style.height = "280px";
    } else {
      heroImg.style.height = "340px";
    }
  }

  adjustHeroImage();
  window.addEventListener("resize", adjustHeroImage);

  /* ===============================
     3D TILT EFFECT (DESKTOP ONLY)
  =============================== */
  if (window.innerWidth > 768) {
    document.querySelectorAll(".hero-img, .about-image").forEach(card => {

      card.addEventListener("mousemove", e => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const rotateY = (x / rect.width - 0.5) * 10;
        const rotateX = (y / rect.height - 0.5) * -10;

        card.style.transform =
          `rotateY(${rotateY}deg) rotateX(${rotateX}deg)`;
      });

      card.addEventListener("mouseleave", () => {
        card.style.transform = "rotateY(0deg) rotateX(0deg)";
      });
    });
  }

  /* ===============================
     COURSE CARD AUTO HEIGHT
  =============================== */
  const courseCards = document.querySelectorAll(".course-card");
  let maxHeight = 0;

  courseCards.forEach(card => {
    card.style.height = "auto";
    maxHeight = Math.max(maxHeight, card.offsetHeight);
  });

  courseCards.forEach(card => {
    card.style.height = maxHeight + "px";
  });

  /* ===============================
     MOBILE NAVBAR TOUCH FEEDBACK
  =============================== */
  document.querySelectorAll(".nav-center a").forEach(link => {
    link.addEventListener("touchstart", () => {
      link.style.opacity = "0.6";
    });
    link.addEventListener("touchend", () => {
      link.style.opacity = "1";
    });
  });

  /* ===============================
     SMOOTH SCROLL FOR INTERNAL LINKS
  =============================== */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      document.querySelector(this.getAttribute("href"))
        ?.scrollIntoView({ behavior: "smooth" });
    });
  });

  /* ===============================
     CONTACT FORM (FRONTEND ONLY)
  =============================== */
  const contactForm = document.querySelector(".contact-form");
  if (contactForm) {
    contactForm.addEventListener("submit", e => {
      e.preventDefault();
      alert("✅ Message sent successfully!");
      contactForm.reset();
    });
  }

  console.log("✅ LMS Base JS loaded successfully");
});
