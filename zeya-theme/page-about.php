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
<section class="zeya-hero"><div class="zeya-hero__media"><img src="<?php echo esc_url( $zeya_images . 'ai-linen.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'ai-linen-640.webp' ); ?> 640w, <?php echo esc_url( $zeya_images . 'ai-linen-1024.webp' ); ?> 1024w, <?php echo esc_url( $zeya_images . 'ai-linen.webp' ); ?> 1122w" sizes="100vw" width="1122" height="1402" alt="Warm linen drapes beside natural stone in a Dubai interior" loading="eager" fetchpriority="high" decoding="async"></div><div class="zeya-hero__scrim" aria-hidden="true"></div><div class="zeya-hero__inner zeya-container"><p class="zeya-hero__eyebrow">The ZEYA story</p><h1 class="zeya-hero__title">A considered finish.<br>A more beautiful everyday.</h1><p class="zeya-hero__sub">Custom curtains, blinds and motorized window solutions, thoughtfully designed for homes and workplaces in Dubai.</p></div></section><section class="zeya-section "><div class="zeya-container zeya-split zeya-split--reverse"><div class="zeya-split__media"><img src="<?php echo esc_url( $zeya_images . 'ai-hero.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'ai-hero-640.webp' ); ?> 640w, <?php echo esc_url( $zeya_images . 'ai-hero-1024.webp' ); ?> 1024w, <?php echo esc_url( $zeya_images . 'ai-hero.webp' ); ?> 1536w" sizes="(max-width:700px) 100vw, 50vw" width="1536" height="1024" alt="A calm living room framed by floor-length curtains" loading="lazy" decoding="async"></div><div class="zeya-split__copy"><p class="zeya-eyebrow">More than window coverings</p><h2>Designed to feel<br>like you.</h2><p>At ZEYA, we believe a well-designed window can transform the way a room feels. Softness, shade, privacy and proportion all have a part to play.</p><p>We take time to understand how you use your space before recommending the right fabric, style or operating system. Every decision is made around your needs.</p><p>From your first fabric sample to the final installation, we keep the process clear, personal and carefully considered.</p><a class="zeya-btn zeya-btn--gold" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>">Let’s talk about your space<svg class="zeya-btn__arrow" aria-hidden="true" focusable="false"><use href="#zeya-i-arrow-right"></use></svg></a></div></div></section><section class="zeya-section zeya-section--chocolate"><div class="zeya-container"><div class="zeya-section-heading"><p class="zeya-eyebrow">Our values</p><div><h2>Care in every detail.</h2></div></div><div class="zeya-steps"><article class="zeya-step"><span class="zeya-step__num">01</span><h3>Personal guidance</h3><p>Options chosen around your light, privacy and daily life.</p></article><article class="zeya-step"><span class="zeya-step__num">02</span><h3>Considered materials</h3><p>Textures and finishes that bring your interior together.</p></article><article class="zeya-step"><span class="zeya-step__num">03</span><h3>A precise finish</h3><p>Accurate measurement and professional installation.</p></article></div></div></section>
<?php
get_footer();
