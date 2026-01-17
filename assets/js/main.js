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
    // Remove preloader immediately when DOM is ready, or after a short timeout if it's already ready
    const removePreloader = () => {
      if (preloader) {
        preloader.remove();
      }
    };

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', removePreloader);
    } else {
      removePreloader();
    }

    // Safety fallback: ensure it's removed after 1 second max even if something hangs
    setTimeout(removePreloader, 1000);

    // Also keeping the load event just in case, but it will likely adhere to the above first
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
