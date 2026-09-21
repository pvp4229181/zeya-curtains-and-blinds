<?php
/**
 * About: split story section, value cards, quote banner and the 'how we work' split.
 *
 * Template Name: ZEYA About
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
<section class="zeya-abouthero">
  <div class="zeya-container zeya-container--wide zeya-abouthero__grid">
    <figure class="zeya-abouthero__media zeya-reveal-mask">
      <img src="<?php echo esc_url( $zeya_images . 'about-zeya-curtains.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'about-zeya-curtains.webp' ); ?> 242w" sizes="(max-width: 1024px) 100vw, 46vw" width="242" height="334" alt="Dining area with full-height sheer curtains, an olive tree and soft morning light" loading="lazy" decoding="async">
    </figure>
    <div class="zeya-abouthero__copy">
      <h1 class="zeya-pagehead__title zeya-reveal">About Us</h1>
      <span class="zeya-rule zeya-reveal" style="--zeya-delay:80ms"></span>
      <nav class="zeya-crumbs" aria-label="Breadcrumb"><a href="<?php echo esc_url( zeya_link( 'home' ) ); ?>">Home</a><span class="zeya-crumbs__sep" aria-hidden="true">/</span><span aria-current="page">About</span></nav>
      <h2 class="zeya-h2" data-zeya-lines>More Than<br>Just Window Coverings</h2>
      <p class="zeya-text zeya-lead zeya-reveal">At ZEYA Curtains &amp; Blinds, we believe windows should be
        more than just covered &mdash; they should be beautifully designed to enhance the way you live and work.</p>
      <p class="zeya-text zeya-reveal">We create custom-made curtains, blinds and motorized window solutions
        that bring together elegance, comfort, privacy and effortless functionality.</p>
      <p class="zeya-text zeya-reveal">From choosing the perfect fabric and style to precise measurement and
        professional installation, we make every step simple, seamless and tailored to your space.</p>
      <p class="zeya-text zeya-reveal">We take the time to understand your space, your style and your practical
        requirements before recommending a suitable solution. Our team guides you through fabrics, colours,
        designs and functionality, followed by accurate measurement and professional installation.</p>
    </div>
  </div>
</section>

<section class="zeya-section zeya-section--sm">
  <div class="zeya-container">
    <div class="zeya-values zeya-stagger">
      <article class="zeya-value"><span class="zeya-value__icon"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-diamond"></use></svg></span><h3 class="zeya-value__title">Quality Craftsmanship</h3></article><article class="zeya-value"><span class="zeya-value__icon"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-people"></use></svg></span><h3 class="zeya-value__title">Personalized Service</h3></article><article class="zeya-value"><span class="zeya-value__icon"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-gear"></use></svg></span><h3 class="zeya-value__title">Modern Solutions</h3></article><article class="zeya-value"><span class="zeya-value__icon"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-heart"></use></svg></span><h3 class="zeya-value__title">Customer Satisfaction</h3></article>
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

<section class="zeya-section zeya-split zeya-split--bleed zeya-split--bleed-right">
  <div class="zeya-container zeya-split__grid">
    <div class="zeya-split__copy">
      <span class="zeya-label zeya-reveal">How We Work</span>
      <h2 class="zeya-h2" data-zeya-lines>Considered at<br>Every Step</h2>
      <p class="zeya-text zeya-reveal">Fabric selection, colour selection, curtain and blind styles,
        measurement, recommendations and professional installation &mdash; each stage is handled by our own
        team, so nothing is left to chance between the first consultation and the finished window.</p>
      <ul class="zeya-list zeya-reveal">
        <li>Fabric selection guided by light, privacy and wear</li>
        <li>Colour and finish matched to your interior</li>
        <li>Curtain and blind styles suited to the room</li>
        <li>On-site measurement by our own team</li>
        <li>Clear recommendations before you commit</li>
        <li>Professional installation and final adjustment</li>
      </ul>
      <div class="zeya-reveal"><a class="zeya-btn zeya-btn--outline" href="<?php echo esc_url( zeya_link( 'process' ) ); ?>">See Our Process<svg class="zeya-btn__arrow" aria-hidden="true" focusable="false"><use href="#zeya-i-arrow-right"></use></svg></a></div>
    </div>
    <figure class="zeya-split__media zeya-split__media--bleed-right zeya-figure zeya-reveal-mask">
      <img src="<?php echo esc_url( $zeya_images . 'fabric-consultation.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'fabric-consultation.webp' ); ?> 148w" sizes="(max-width: 1024px) 100vw, 50vw" width="148" height="97" alt="Stacked curtain fabric samples in warm neutral tones" loading="lazy" decoding="async">
    </figure>
  </div>
</section>
<?php
get_footer();
