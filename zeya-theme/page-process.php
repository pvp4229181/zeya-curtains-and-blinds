<?php
/**
 * Process: page header, consultation photograph, six-step timeline, gallery and closing line.
 *
 * Template Name: ZEYA Process
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
<section class="zeya-pagehead">
  <div class="zeya-container zeya-pagehead__grid">
    <div class="zeya-pagehead__left zeya-reveal">
      <h1 class="zeya-pagehead__title">Our Process</h1>
      <span class="zeya-rule"></span>
      <nav class="zeya-crumbs" aria-label="Breadcrumb"><a href="<?php echo esc_url( zeya_link( 'home' ) ); ?>">Home</a><span class="zeya-crumbs__sep" aria-hidden="true">/</span><span aria-current="page">Process</span></nav>
    </div>
    <div class="zeya-pagehead__right zeya-reveal" style="--zeya-delay:120ms">
      <h2 class="zeya-pagehead__lead">A simple process designed<br>around your convenience.</h2>
      <p class="zeya-pagehead__text">Six clear steps from first enquiry to the final fitting, handled end to end by the ZEYA team.</p>
    </div>
  </div>
</section>

<section class="zeya-section zeya-section--sm" style="padding-top:0">
  <div class="zeya-container">
    <figure class="zeya-process__hero zeya-reveal-mask">
      <img src="<?php echo esc_url( $zeya_images . 'process-consultation.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'process-consultation.webp' ); ?> 474w" sizes="(max-width: 1320px) 100vw, 1320px" width="474" height="124" alt="ZEYA consultant showing curtain fabric samples to a customer at a table" loading="lazy" decoding="async">
    </figure>

    <ol class="zeya-timeline zeya-mt zeya-stagger">
      
<li class="zeya-step">
  <span class="zeya-step__icon"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-calendar"></use></svg></span>
  <span class="zeya-step__num">01</span>
  <h3 class="zeya-step__title">Book a Free Consultation</h3>
  <p class="zeya-step__text">Contact us through WhatsApp, phone or our enquiry form.</p>
</li>
<li class="zeya-step">
  <span class="zeya-step__icon"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-home"></use></svg></span>
  <span class="zeya-step__num">02</span>
  <h3 class="zeya-step__title">We Visit Your Space</h3>
  <p class="zeya-step__text">Our team visits your home, office or project with relevant samples and recommendations.</p>
</li>
<li class="zeya-step">
  <span class="zeya-step__icon"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-swatch"></use></svg></span>
  <span class="zeya-step__num">03</span>
  <h3 class="zeya-step__title">Choose Your Solution</h3>
  <p class="zeya-step__text">Select your preferred fabric, colour, curtain style, blind or motorized system.</p>
</li>
<li class="zeya-step">
  <span class="zeya-step__icon"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-ruler"></use></svg></span>
  <span class="zeya-step__num">04</span>
  <h3 class="zeya-step__title">Accurate Measurement</h3>
  <p class="zeya-step__text">We take precise measurements for your windows.</p>
</li>
<li class="zeya-step">
  <span class="zeya-step__icon"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-doc"></use></svg></span>
  <span class="zeya-step__num">05</span>
  <h3 class="zeya-step__title">Quotation &amp; Approval</h3>
  <p class="zeya-step__text">You receive a clear quotation based on your selected solution.</p>
</li>
<li class="zeya-step">
  <span class="zeya-step__icon"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-tools"></use></svg></span>
  <span class="zeya-step__num">06</span>
  <h3 class="zeya-step__title">Professional Installation</h3>
  <p class="zeya-step__text">Once approved, our team prepares and installs your curtains or blinds.</p>
</li>
    </ol>

    <div class="zeya-gallery zeya-mt zeya-stagger">
      <figure class="zeya-figure zeya-reveal"><img src="<?php echo esc_url( $zeya_images . 'fabric-consultation.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'fabric-consultation.webp' ); ?> 148w" sizes="(max-width: 560px) 100vw, (max-width: 860px) 100vw, 33vw" width="148" height="97" alt="Curtain fabric samples fanned out in warm neutral tones" loading="lazy" decoding="async"></figure>
      <figure class="zeya-figure zeya-reveal"><img src="<?php echo esc_url( $zeya_images . 'window-measurement.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'window-measurement.webp' ); ?> 150w" sizes="(max-width: 860px) 50vw, 33vw" width="150" height="97" alt="ZEYA team member measuring a full-height window" loading="lazy" decoding="async"></figure>
      <figure class="zeya-figure zeya-reveal"><img src="<?php echo esc_url( $zeya_images . 'curtain-installation.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'curtain-installation.webp' ); ?> 151w" sizes="(max-width: 860px) 50vw, 33vw" width="151" height="97" alt="ZEYA installer fitting a curtain track above a bright window" loading="lazy" decoding="async"></figure>
    </div>

    <p class="zeya-closing zeya-mt zeya-measure zeya-mx-auto" data-zeya-lines>You choose the look.<br>We take care of the details.</p>
  </div>
</section>
<?php
get_footer();
