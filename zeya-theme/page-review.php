<?php
/**
 * Review: the thank-you hero with ZEYA's message, the Google review button and three steps.
 *
 * Template Name: ZEYA Review
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
<section class="zeya-hero zeya-hero--product"><div class="zeya-hero__media"><img src="<?php echo esc_url( $zeya_images . 'ai-sheer.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'ai-sheer-640.webp' ); ?> 640w, <?php echo esc_url( $zeya_images . 'ai-sheer-1024.webp' ); ?> 1024w, <?php echo esc_url( $zeya_images . 'ai-sheer.webp' ); ?> 1122w" sizes="100vw" width="1122" height="1402" alt="Softly lit sheer curtains in a Dubai apartment" loading="eager" fetchpriority="high" decoding="async"></div><div class="zeya-hero__scrim" aria-hidden="true"></div><div class="zeya-hero__inner zeya-container"><p class="zeya-hero__eyebrow">Share your experience</p><h1 class="zeya-hero__title">Thank you for<br>choosing ZEYA.</h1><p class="zeya-hero__sub">We&rsquo;d love to hear about your experience with us. Your feedback means a lot to our team and encourages us to keep delivering exceptional service.</p><div class="zeya-hero__actions"><a class="zeya-btn zeya-btn--gold zeya-btn--review" data-zeya-review hidden><svg aria-hidden="true" focusable="false"><use href="#zeya-i-star"></use></svg>Write a Google review</a><span data-zeya-review-fallback><a class="zeya-btn zeya-btn--gold" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>">Share your feedback<svg class="zeya-btn__arrow" aria-hidden="true" focusable="false"><use href="#zeya-i-arrow-right"></use></svg></a></span></div></div></section><section class="zeya-section "><div class="zeya-container"><div class="zeya-section-heading"><p class="zeya-eyebrow">It takes a minute</p><div><h2>Three quick steps.</h2></div></div><div class="zeya-steps"><article class="zeya-step"><span class="zeya-step__num">01</span><h3>Open the review form</h3><p>Tap &ldquo;Write a Google review&rdquo; and Google opens ZEYA&rsquo;s review form. You may be asked to sign in to your Google account.</p></article><article class="zeya-step"><span class="zeya-step__num">02</span><h3>Choose your stars</h3><p>Rate your experience, from the first visit to the finished installation.</p></article><article class="zeya-step"><span class="zeya-step__num">03</span><h3>Add a few words</h3><p>Tell others what stood out, then tap Post. Thank you &mdash; it means a great deal to us.</p></article></div></div></section>
<?php
get_footer();
