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
<section class="zeya-contact">
  <div class="zeya-container zeya-container--wide zeya-contact__grid">

    <div class="zeya-contact__copy">
      <h1 class="zeya-pagehead__title zeya-reveal">Contact Us</h1>
      <span class="zeya-rule zeya-reveal" style="--zeya-delay:80ms"></span>
      <nav class="zeya-crumbs" aria-label="Breadcrumb"><a href="<?php echo esc_url( zeya_link( 'home' ) ); ?>">Home</a><span class="zeya-crumbs__sep" aria-hidden="true">/</span><span aria-current="page">Contact</span></nav>
      <h2 class="zeya-h2" data-zeya-lines>Let&rsquo;s Transform<br>Your Windows</h2>
      <p class="zeya-text zeya-lead zeya-reveal">Not sure which curtains or blinds are right for your space?</p>
      <p class="zeya-text zeya-reveal">Our team can help you select the right combination of style, fabric,
        privacy, light control and functionality.</p>
      <p class="zeya-text zeya-reveal">Book a consultation and let us bring the options to you.</p>

      <div class="zeya-methods zeya-reveal">
        
<a class="zeya-method" data-zeya-contact="address">
  <span class="zeya-method__icon"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-pin"></use></svg></span>
  <span>
    <span class="zeya-method__label">Dubai, UAE</span>
    <span class="zeya-method__value" data-zeya-contact-value></span>
  </span>
</a>
<a class="zeya-method" data-zeya-contact="whatsapp">
  <span class="zeya-method__icon"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-whatsapp"></use></svg></span>
  <span>
    <span class="zeya-method__label">WhatsApp</span>
    <span class="zeya-method__value" data-zeya-contact-value></span>
  </span>
</a>
<a class="zeya-method" data-zeya-contact="phone">
  <span class="zeya-method__icon"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-phone"></use></svg></span>
  <span>
    <span class="zeya-method__label">Phone</span>
    <span class="zeya-method__value" data-zeya-contact-value></span>
  </span>
</a>
<a class="zeya-method" data-zeya-contact="email">
  <span class="zeya-method__icon"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-mail"></use></svg></span>
  <span>
    <span class="zeya-method__label">Email</span>
    <span class="zeya-method__value" data-zeya-contact-value></span>
  </span>
</a>
      </div>

      <div class="zeya-contact__actions zeya-reveal">
        <a class="zeya-btn zeya-btn--gold" href="#zeya-name">Book a Free Consultation<svg class="zeya-btn__arrow" aria-hidden="true" focusable="false"><use href="#zeya-i-arrow-right"></use></svg></a>
      </div>
    </div>

    <div class="zeya-contact__panel">
      <div class="zeya-contact__panel-media" aria-hidden="true">
        <img src="<?php echo esc_url( $zeya_images . 'contact-interior.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'contact-interior.webp' ); ?> 116w" sizes="(max-width: 1024px) 100vw, 46vw" width="116" height="211" alt="Dubai apartment interior with sheer curtains and skyline views" loading="lazy" decoding="async">
      </div>

      <div class="zeya-formcard zeya-reveal">
        <h2 class="zeya-formcard__title">Send Us a Message</h2>

        <?php if ( zeya_has_form_plugin() ) : ?>
          <?php echo do_shortcode( zeya_contact_form_shortcode() ); ?>
        <?php else : ?>
          <!-- Field names follow the Contact Form 7 / WPForms convention so this
             markup can be swapped for a plugin-rendered form without restyling.
             `action` is intentionally empty until a real handler is connected. -->
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
        <?php endif; ?>
      </div>
    </div>

  </div>
</section>
<?php
get_footer();
