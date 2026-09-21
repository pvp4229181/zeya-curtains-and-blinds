<?php
/**
 * Front page: hero, benefits strip, introduction split, product cards and quote banner.
 *
 * @package ZEYA
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

// Base URL for this theme's images; every <img> below builds on it.
$zeya_images = zeya_asset( 'images/' );
?>
<section class="zeya-hero" data-zeya-hero>
  <div class="zeya-hero__media" data-zeya-parallax="0.07">
    <img src="<?php echo esc_url( $zeya_images . 'hero-luxury-curtains.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'hero-luxury-curtains.webp' ); ?> 160w" sizes="100vw" width="160" height="136" alt="Sunlit Dubai living room with floor-to-ceiling windows, layered sheer and blackout curtains and the city skyline beyond" loading="eager" fetchpriority="high" decoding="async">
  </div>
  <div class="zeya-hero__overlay" aria-hidden="true"></div>

  <div class="zeya-container zeya-container--wide zeya-hero__inner">
    <div class="zeya-hero__copy">
      <h1 class="zeya-hero__title" data-zeya-lines>Custom Curtains,<br>Blinds &amp; Motorized<br>Window Solutions<br>in Dubai</h1>
      <p class="zeya-hero__sub">Elegant. Functional. Made for Your Space.</p>
      <div class="zeya-hero__actions">
        <a class="zeya-btn zeya-btn--gold" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>">Book a Free Consultation<svg class="zeya-btn__arrow" aria-hidden="true" focusable="false"><use href="#zeya-i-arrow-right"></use></svg></a>
      </div>
    </div>
  </div>

  <div class="zeya-container zeya-container--wide zeya-hero__foot">
    <ol class="zeya-hero__slides" role="presentation">
      <li class="zeya-hero__slide is-active" data-zeya-hero-mark>01</li>
      <li class="zeya-hero__slide" data-zeya-hero-mark>02</li>
      <li class="zeya-hero__slide" data-zeya-hero-mark>03</li>
    </ol>
    <p class="zeya-hero__tag">Transforming Spaces<br>Through Beautiful Windows</p>
  </div>
</section>

<section class="zeya-benefits" aria-labelledby="zeya-benefits-heading"><h2 class="zeya-sr-only" id="zeya-benefits-heading">Why clients choose ZEYA</h2><div class="zeya-container zeya-container--wide zeya-benefits__grid zeya-stagger"><article class="zeya-benefit zeya-reveal"><span class="zeya-benefit__icon"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-diamond"></use></svg></span><h3 class="zeya-benefit__title">Premium Quality<br>Materials</h3></article><article class="zeya-benefit zeya-reveal"><span class="zeya-benefit__icon"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-home"></use></svg></span><h3 class="zeya-benefit__title">Custom Made<br>for Your Space</h3></article><article class="zeya-benefit zeya-reveal"><span class="zeya-benefit__icon"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-gear"></use></svg></span><h3 class="zeya-benefit__title">Motorized<br>Solutions</h3></article><article class="zeya-benefit zeya-reveal"><span class="zeya-benefit__icon"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-heart"></use></svg></span><h3 class="zeya-benefit__title">Elegant &amp; Functional<br>Designs</h3></article></div></section>

<section class="zeya-section zeya-split zeya-split--bleed zeya-split--bleed-left">
  <div class="zeya-container zeya-split__grid">
    <figure class="zeya-split__media zeya-split__media--bleed-left zeya-figure zeya-reveal-mask">
      <img src="<?php echo esc_url( $zeya_images . 'intro-living-room.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'intro-living-room.webp' ); ?> 278w" sizes="(max-width: 1024px) 100vw, 52vw" width="278" height="144" alt="Bright neutral living room with sheer curtains diffusing daylight across a linen sofa" loading="lazy" decoding="async">
    </figure>
    <div class="zeya-split__copy">
      <h2 class="zeya-h2 zeya-split__title" data-zeya-lines>Beautiful Windows<br>Brighter Living</h2>
      <p class="zeya-text zeya-lead zeya-reveal">At ZEYA, we create custom-made curtains and blinds that bring
        elegance, comfort and functionality to your home or workspace.</p>
      <p class="zeya-text zeya-reveal">Every project starts with your space. We guide you through fabrics,
        colours, styles and light control, then measure accurately and install professionally &mdash; so the
        finished result looks considered and works effortlessly, every day.</p>
      <div class="zeya-reveal"><a class="zeya-btn zeya-btn--gold" href="<?php echo esc_url( zeya_link( 'products' ) ); ?>">Explore Our Products<svg class="zeya-btn__arrow" aria-hidden="true" focusable="false"><use href="#zeya-i-arrow-right"></use></svg></a></div>
    </div>
  </div>
</section>

<section class="zeya-section zeya-section--cream">
  <div class="zeya-container">
    <div class="zeya-center zeya-measure zeya-mx-auto zeya-reveal">
      <span class="zeya-label">What We Do</span>
      <h2 class="zeya-h2 zeya-mt-sm">Complete Curtains &amp; Blinds Solutions</h2>
      <p class="zeya-text zeya-mx-auto zeya-mt-sm">From timeless curtains to modern automated blinds, ZEYA
        offers a range of window solutions for different interiors, requirements and budgets.</p>
    </div>
    <div class="zeya-cards zeya-mt zeya-stagger">
      
<article class="zeya-card zeya-reveal">
  <a class="zeya-card__link" href="<?php echo esc_url( zeya_link( 'curtains' ) ); ?>">
    <img class="zeya-card__img" src="<?php echo esc_url( $zeya_images . 'curtains-category.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'curtains-category.webp' ); ?> 154w" sizes="(max-width: 560px) 100vw, (max-width: 860px) 50vw, 33vw" width="154" height="118" alt="Layered curtains in warm neutral fabric beside a sunlit window" loading="lazy" decoding="async">
    <span class="zeya-card__veil" aria-hidden="true"></span>
    <div class="zeya-card__body">
      <div>
        <h3 class="zeya-card__title">Curtains</h3>
        <p class="zeya-card__text">Elegant fabrics for every space</p>
      </div>
      <span class="zeya-arrow-btn" aria-hidden="true"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-arrow-right"></use></svg></span>
    </div>
  </a>
</article>
<article class="zeya-card zeya-reveal">
  <a class="zeya-card__link" href="<?php echo esc_url( zeya_link( 'blinds' ) ); ?>">
    <img class="zeya-card__img" src="<?php echo esc_url( $zeya_images . 'blinds-category.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'blinds-category.webp' ); ?> 153w" sizes="(max-width: 560px) 100vw, (max-width: 860px) 50vw, 33vw" width="153" height="118" alt="Horizontal slat blinds filtering daylight in a modern interior" loading="lazy" decoding="async">
    <span class="zeya-card__veil" aria-hidden="true"></span>
    <div class="zeya-card__body">
      <div>
        <h3 class="zeya-card__title">Blinds</h3>
        <p class="zeya-card__text">Modern &amp; versatile options</p>
      </div>
      <span class="zeya-arrow-btn" aria-hidden="true"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-arrow-right"></use></svg></span>
    </div>
  </a>
</article>
<article class="zeya-card zeya-reveal">
  <a class="zeya-card__link" href="<?php echo esc_url( zeya_link( 'motorized' ) ); ?>">
    <img class="zeya-card__img" src="<?php echo esc_url( $zeya_images . 'motorized-solutions.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'motorized-solutions.webp' ); ?> 152w" sizes="(max-width: 560px) 100vw, (max-width: 860px) 50vw, 33vw" width="152" height="118" alt="Motorized blind lowering over a city view, controlled from a phone" loading="lazy" decoding="async">
    <span class="zeya-card__veil" aria-hidden="true"></span>
    <div class="zeya-card__body">
      <div>
        <h3 class="zeya-card__title">Motorized Solutions</h3>
        <p class="zeya-card__text">Smart living made simple</p>
      </div>
      <span class="zeya-arrow-btn" aria-hidden="true"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-arrow-right"></use></svg></span>
    </div>
  </a>
</article>
    </div>
  </div>
</section>


<section class="zeya-quote">
  <div class="zeya-quote__media" data-zeya-parallax="0.09">
    <img src="<?php echo esc_url( $zeya_images . 'quote-banner-fabric.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'quote-banner-fabric.webp' ); ?> 491w" sizes="100vw" width="491" height="35" alt="Close detail of softly folded curtain fabric catching warm side light" loading="lazy" decoding="async">
  </div>
  <div class="zeya-container zeya-quote__grid">
    <blockquote class="zeya-quote__text" data-zeya-lines>&ldquo;Beautiful Spaces<br>Start at the Window&rdquo;</blockquote>
    <div class="zeya-quote__note zeya-reveal">
      <p>&ldquo;Our mission is to bring style, comfort and innovation to every space we touch.&rdquo;</p>
      <cite class="zeya-quote__cite">&mdash; ZEYA Curtains &amp; Blinds</cite>
    </div>
  </div>
</section>
<?php
get_footer();
