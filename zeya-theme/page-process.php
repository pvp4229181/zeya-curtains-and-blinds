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
<section class="zeya-hero"><div class="zeya-hero__media"><img src="<?php echo esc_url( $zeya_images . 'ai-consultation.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'ai-consultation-640.webp' ); ?> 640w, <?php echo esc_url( $zeya_images . 'ai-consultation-1024.webp' ); ?> 1024w, <?php echo esc_url( $zeya_images . 'ai-consultation.webp' ); ?> 1536w" sizes="100vw" width="1536" height="1024" alt="Fabric selection during an interior design consultation" loading="eager" fetchpriority="high" decoding="async"></div><div class="zeya-hero__scrim" aria-hidden="true"></div><div class="zeya-hero__inner zeya-container"><p class="zeya-hero__eyebrow">From first idea to final installation</p><h1 class="zeya-hero__title">A beautiful result.<br>A simple journey.</h1><p class="zeya-hero__sub">We guide you through every decision, so choosing your curtains and blinds feels as good as the finished space.</p></div></section><section class="zeya-section "><div class="zeya-container"><ol class="zeya-process"><li class="zeya-process__step"><span class="zeya-process__num">01</span><div><h2>A conversation</h2><p>Tell us about your space, your style and the way you want to live.</p></div></li><li class="zeya-process__step"><span class="zeya-process__num">02</span><div><h2>A visit to your space</h2><p>We bring relevant samples and recommendations to your home or workplace.</p></div></li><li class="zeya-process__step"><span class="zeya-process__num">03</span><div><h2>Your perfect combination</h2><p>Choose your fabric, finish, light control and operating system.</p></div></li><li class="zeya-process__step"><span class="zeya-process__num">04</span><div><h2>Measured with care</h2><p>We take precise window measurements and plan the fitting details.</p></div></li><li class="zeya-process__step"><span class="zeya-process__num">05</span><div><h2>A clear quotation</h2><p>Review the specification and quotation before you approve your order.</p></div></li><li class="zeya-process__step"><span class="zeya-process__num">06</span><div><h2>The finishing touch</h2><p>Your curtains or blinds are prepared and professionally installed.</p></div></li></ol></div></section><section class="zeya-section zeya-section--chocolate"><div class="zeya-container zeya-split"><div class="zeya-split__copy"><p class="zeya-eyebrow">The details make the difference</p><h2>See it. Feel it.<br>Make it yours.</h2><p>Explore colour, texture and light together. We will help you find a combination that feels right in your own space.</p><a class="zeya-btn zeya-btn--gold" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>">Book a consultation<svg class="zeya-btn__arrow" aria-hidden="true" focusable="false"><use href="#zeya-i-arrow-right"></use></svg></a></div><div class="zeya-split__media"><img src="<?php echo esc_url( $zeya_images . 'signature-fabric.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'signature-fabric-640.webp' ); ?> 640w, <?php echo esc_url( $zeya_images . 'signature-fabric-1024.webp' ); ?> 1024w, <?php echo esc_url( $zeya_images . 'signature-fabric.webp' ); ?> 1536w" sizes="(max-width:700px) 100vw, 50vw" width="1536" height="1024" alt="Linen, sheer and velvet fabric samples" loading="lazy" decoding="async"></div></div></section>
<?php
get_footer();
