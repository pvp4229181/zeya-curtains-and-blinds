<?php
/**
 * Contact: enquiry copy, contact methods and the form card over the interior panel.
 *
 * Template Name: ZEYA Contact
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
<section class="zeya-hero"><div class="zeya-hero__media"><img src="<?php echo esc_url( $zeya_images . 'signature-curtains.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'signature-curtains-640.webp' ); ?> 640w, <?php echo esc_url( $zeya_images . 'signature-curtains-1024.webp' ); ?> 1024w, <?php echo esc_url( $zeya_images . 'signature-curtains.webp' ); ?> 1536w" sizes="100vw" width="1536" height="1024" alt="Softly lit sheer curtains in a Dubai apartment" loading="eager" fetchpriority="high" decoding="async"></div><div class="zeya-hero__scrim" aria-hidden="true"></div><div class="zeya-hero__inner zeya-container"><p class="zeya-hero__eyebrow">Let’s create something beautiful</p><h1 class="zeya-hero__title">Your space.<br>Our next conversation.</h1><p class="zeya-hero__sub">Tell us what you have in mind. We’ll help you explore the fabrics, finishes and window solutions that suit your space.</p></div></section><section class="zeya-section "><div class="zeya-container zeya-contact"><div class="zeya-contact__aside"><img src="<?php echo esc_url( $zeya_images . 'signature-curtains.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'signature-curtains-640.webp' ); ?> 640w, <?php echo esc_url( $zeya_images . 'signature-curtains-1024.webp' ); ?> 1024w, <?php echo esc_url( $zeya_images . 'signature-curtains.webp' ); ?> 1536w" sizes="(max-width:700px) 100vw, 45vw" width="1536" height="1024" alt="Sheer curtains diffusing afternoon light" loading="lazy" decoding="async"><div class="zeya-contact__info"><h2>Based in Dubai.<br>Designed around you.</h2><p>Home, office or commercial space — we begin with your needs.</p><div class="zeya-methods"><a class="zeya-method" data-zeya-contact="address"><span>Studio</span><span data-zeya-contact-value></span></a><a class="zeya-method" data-zeya-contact="phone"><span>Phone</span><span data-zeya-contact-value></span></a><a class="zeya-method" data-zeya-contact="whatsapp"><span>WhatsApp</span><span data-zeya-contact-value></span></a><a class="zeya-method" data-zeya-contact="email"><span>Email</span><span data-zeya-contact-value></span></a></div></div></div><div class="zeya-formcard"><p class="zeya-eyebrow">Start your project</p><h2>Tell us about your space.</h2><p class="zeya-form-intro">Share a few details and the products you’re considering.</p><?php if ( zeya_has_form_plugin() ) : ?>
          <?php echo do_shortcode( zeya_contact_form_shortcode() ); ?>
        <?php else : ?>
          <form class="zeya-form" data-zeya-form action="<?php echo esc_url( zeya_contact( 'formEndpoint' ) ); ?>" method="post" novalidate>
          <p class="zeya-hp" aria-hidden="true">
            <label>Leave this field empty<input type="text" name="zeya-website-url" tabindex="-1"
                   autocomplete="off" data-zeya-hp></label>
          </p>

          <div class="zeya-field">
            <label class="zeya-field__label" for="zeya-name">Your Name</label>
            <input class="zeya-input" id="zeya-name" name="your-name" type="text"
                   autocomplete="name" placeholder="Your Name" required>
            <p class="zeya-field__error" id="zeya-name-error" role="alert"></p>
          </div>

          <div class="zeya-field">
            <label class="zeya-field__label" for="zeya-email">Your Email</label>
            <input class="zeya-input" id="zeya-email" name="your-email" type="email"
                   autocomplete="email" placeholder="Your Email" required>
            <p class="zeya-field__error" id="zeya-email-error" role="alert"></p>
          </div>

          <div class="zeya-field">
            <label class="zeya-field__label" for="zeya-phone">Your Phone</label>
            <input class="zeya-input" id="zeya-phone" name="your-phone" type="tel"
                   autocomplete="tel" placeholder="Your Phone" required>
            <p class="zeya-field__error" id="zeya-phone-error" role="alert"></p>
          </div>

          <div class="zeya-field">
            <label class="zeya-field__label" for="zeya-message">Your Message</label>
            <textarea class="zeya-textarea" id="zeya-message" name="your-message" rows="4"
                      placeholder="Tell us about your space" required></textarea>
            <p class="zeya-field__error" id="zeya-message-error" role="alert"></p>
          </div>

          <button class="zeya-btn zeya-btn--gold zeya-btn--block" type="submit">
            Send Message <svg class="zeya-btn__arrow" aria-hidden="true" focusable="false"><use href="#zeya-i-arrow-right"></use></svg>
          </button>

          <p class="zeya-form__status" data-zeya-form-status data-state="info" role="status" aria-live="polite"></p>
        </form>
        <?php endif; ?></div></div></section>
<?php
get_footer();
