/**
* Template Name: UpConstruction-1
* Template URL: https://bootstrapmade.com/upconstruction-bootstrap-construction-website-template/
* Updated: Aug 07 2024 with Bootstrap v5.3.3
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function () {
  "use strict";

  /**
   * Page Loading Bar and Transitions (Branded)
   */
  const loadingBar = document.createElement('div');
  loadingBar.id = 'top-loading-bar';
  document.body.prepend(loadingBar);

  let loadingProgress = 10;
  const updateProgress = (target) => {
    loadingProgress = Math.min(target, 100);
    if (loadingBar) loadingBar.style.width = loadingProgress + '%';
    if (loadingProgress === 100 && loadingBar) {
      setTimeout(() => {
        loadingBar.style.opacity = '0';
        setTimeout(() => loadingBar.remove(), 500);
      }, 300);
    }
  };

  // Initial progress on DOM Ready
  document.addEventListener('DOMContentLoaded', () => {
    updateProgress(60);
  });

  // Final progress on window load
  window.addEventListener('load', () => {
    updateProgress(100);
  });

  // Handle Branded Page Exit Transitions
  document.addEventListener('click', (e) => {
    const link = e.target.closest('a');
    if (link &&
      link.href &&
      link.href.startsWith(window.location.origin) &&
      !link.href.includes('#') &&
      link.target !== '_blank' &&
      !e.ctrlKey && !e.shiftKey && !e.metaKey) {

      e.preventDefault();

      // Show original preloader for branded transition
      let preloader = document.querySelector('#preloader');
      if (!preloader) {
        preloader = document.createElement('div');
        preloader.id = 'preloader';
        document.body.appendChild(preloader);
      }

      document.body.classList.add('page-transitioning');
      preloader.style.opacity = '0';
      preloader.style.display = 'block';
      preloader.style.visibility = 'visible';

      // Fast fade-in of spinner
      requestAnimationFrame(() => {
        preloader.style.transition = 'opacity 0.4s ease';
        preloader.style.opacity = '1';
      });

      setTimeout(() => {
        window.location.href = link.href;
      }, 400);
    }
  });

  // Handle back-forward cache
  window.addEventListener('pageshow', (event) => {
    if (event.persisted) {
      const preloader = document.querySelector('#preloader');
      if (preloader) preloader.remove();
      document.body.classList.remove('page-transitioning');
    }
  });

  /**
   * Apply .scrolled class to the body as the page is scrolled down
   */
  function toggleScrolled() {
    const selectBody = document.querySelector('body');
    const selectHeader = document.querySelector('#header');
    if (!selectHeader) return;
    if (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top')) return;
    window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
  }

  document.addEventListener('scroll', toggleScrolled);
  window.addEventListener('load', toggleScrolled);

  /**
   * Mobile nav toggle
   */
  const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    if (!mobileNavToggleBtn) return;
    mobileNavToggleBtn.classList.toggle('bi-list');
    mobileNavToggleBtn.classList.toggle('bi-x');
  }
  if (mobileNavToggleBtn) {
    mobileNavToggleBtn.addEventListener('click', mobileNavToogle);
  }

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navmenu a').forEach(navmenu => {
    navmenu.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });

  });

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
    navmenu.addEventListener('click', function (e) {
      e.preventDefault();
      this.parentNode.classList.toggle('active');
      this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
      e.stopImmediatePropagation();
    });
  });

  /**
   * Preloader
   */
  /**
   * Preloader
   */
  const preloader = document.querySelector('#preloader');
  if (preloader) {
    const removePreloader = () => {
      if (preloader) {
        preloader.style.transition = 'opacity 0.5s ease';
        preloader.style.opacity = '0';
        setTimeout(() => {
          if (preloader.parentNode) preloader.remove();
        }, 500);
      }
    };

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', removePreloader);
    } else {
      removePreloader();
    }

    setTimeout(removePreloader, 1000);
    window.addEventListener('load', removePreloader);
  }

  /**
   * Scroll top button
   */
  let scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  if (scrollTop) {
    scrollTop.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    if (typeof AOS !== 'undefined' && AOS && typeof AOS.init === 'function') {
      AOS.init({
        duration: 400, // Reduced from 600 for snappy feel
        offset: 50,    // Reduced offset to trigger sooner
        easing: 'ease-in-out',
        once: true,
        mirror: false
      });
    }
  }
  // Initialize on DOMContentLoaded for faster start, irrelevant of images loading
  document.addEventListener('DOMContentLoaded', aosInit);

  /**
   * Initiate glightbox
   */
  let glightbox = null;
  if (typeof GLightbox !== 'undefined') {
    glightbox = GLightbox({ selector: '.glightbox' });
  }

  /**
   * Init isotope layout and filters
   */
  document.querySelectorAll('.isotope-layout').forEach(function (isotopeItem) {
    let layout = isotopeItem.getAttribute('data-layout') ?? 'masonry';
    let filter = isotopeItem.getAttribute('data-default-filter') ?? '*';
    let sort = isotopeItem.getAttribute('data-sort') ?? 'original-order';

    let initIsotope;
    const isotopeContainer = isotopeItem.querySelector('.isotope-container');
    if (!isotopeContainer) return;

    // Initialize Isotope immediately with the default filter
    initIsotope = new Isotope(isotopeContainer, {
      itemSelector: '.isotope-item',
      layoutMode: layout,
      filter: filter,
      sortBy: sort
    });

    // Re-layout when images are loaded
    if (typeof imagesLoaded === 'function') {
      imagesLoaded(isotopeContainer, function () {
        initIsotope.layout();
      });
    }

    isotopeItem.querySelectorAll('.isotope-filters li').forEach(function (filters) {
      filters.addEventListener('click', function () {
        isotopeItem.querySelector('.isotope-filters .filter-active').classList.remove('filter-active');
        this.classList.add('filter-active');
        initIsotope.arrange({
          filter: this.getAttribute('data-filter')
        });
        if (typeof aosInit === 'function') {
          aosInit();
        }
      }, false);
    });

  });

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    if (typeof Swiper !== 'undefined') {
      document.querySelectorAll(".init-swiper").forEach(function (swiperElement) {
        const configEl = swiperElement.querySelector(".swiper-config");
        if (!configEl) return;
        let config = {};
        try {
          config = JSON.parse(configEl.innerHTML.trim());
        } catch (e) {
          return;
        }

        if (swiperElement.classList.contains("swiper-tab") && typeof initSwiperWithCustomPagination === 'function') {
          initSwiperWithCustomPagination(swiperElement, config);
        } else {
          new Swiper(swiperElement, config);
        }
      });
    }
  }

  window.addEventListener("load", initSwiper);

  /**
   * Initiate Pure Counter
   */
  new PureCounter();

})();
