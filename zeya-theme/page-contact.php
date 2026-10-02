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
<section class="zeya-hero"><div class="zeya-hero__media"><img src="<?php echo esc_url( $zeya_images . 'ai-sheer.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'ai-sheer-640.webp' ); ?> 640w, <?php echo esc_url( $zeya_images . 'ai-sheer-1024.webp' ); ?> 1024w, <?php echo esc_url( $zeya_images . 'ai-sheer.webp' ); ?> 1536w" sizes="100vw" width="1536" height="1024" alt="Softly lit sheer curtains in a Dubai apartment" loading="eager" fetchpriority="high" decoding="async"></div><div class="zeya-hero__scrim" aria-hidden="true"></div><div class="zeya-hero__inner zeya-container"><p class="zeya-hero__eyebrow">Let’s create something beautiful</p><h1 class="zeya-hero__title">Your space.<br>Our next conversation.</h1><p class="zeya-hero__sub">Tell us what you have in mind. We’ll help you explore the fabrics, finishes and window solutions that suit your space.</p></div></section><section class="zeya-section "><div class="zeya-container zeya-contact"><div class="zeya-contact__aside"><img src="<?php echo esc_url( $zeya_images . 'ai-sheer.webp' ); ?>" srcset="<?php echo esc_url( $zeya_images . 'ai-sheer-640.webp' ); ?> 640w, <?php echo esc_url( $zeya_images . 'ai-sheer-1024.webp' ); ?> 1024w, <?php echo esc_url( $zeya_images . 'ai-sheer.webp' ); ?> 1536w" sizes="(max-width:700px) 100vw, 45vw" width="1536" height="1024" alt="Sheer curtains diffusing afternoon light" loading="lazy" decoding="async"><div class="zeya-contact__info"><h2>Based in Dubai.<br>Designed around you.</h2><p>Home, office or commercial space — we begin with your needs.</p><div class="zeya-methods"><a class="zeya-method" data-zeya-contact="address"><span>Studio</span><span data-zeya-contact-value></span></a><div class="zeya-method" data-zeya-contact="hours"><span>Hours</span><span data-zeya-contact-value></span></div><a class="zeya-method" data-zeya-contact="call"><span>Phone</span><span data-zeya-contact-value></span></a><a class="zeya-method" data-zeya-contact="whatsapp"><span>WhatsApp</span><span data-zeya-contact-value></span></a><a class="zeya-method" data-zeya-contact="email"><span>Email</span><span data-zeya-contact-value></span></a></div></div></div><div class="zeya-formcard"><p class="zeya-eyebrow">Start your project</p><h2>Tell us about your space.</h2><p class="zeya-form-intro">Share a few details and the products you’re considering.</p><?php if ( zeya_has_form_plugin() ) : ?>
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
        <?php endif; ?></div></div></section><section class="zeya-areas" id="service-areas" aria-labelledby="zeya-areas-title">
  <div class="zeya-container">
    <div class="zeya-areas__top">
      <div class="zeya-areas__copy">
        <p class="zeya-eyebrow">We come to you</p>
        <h2 id="zeya-areas-title">Service Areas<br>We Cover</h2>
        <p class="zeya-areas__lead">From waterfront apartments to family villas, our team brings samples, advice and precise measuring directly to your space.</p>
        <p class="zeya-areas__note"><strong>29</strong><span>Dubai communities<br>and the wider UAE</span></p>
      </div>
      <div class="zeya-areas__media">
        <video class="zeya-areas__video" data-zeya-motion-video data-src="<?php echo esc_url( zeya_asset( 'videos/zeya-brand-film.mp4' ) ); ?>" poster="<?php echo esc_url( $zeya_images . 'zeya-brand-film-poster.webp' ); ?>" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1"></video>
        <span class="zeya-areas__film-label">Across Dubai</span>
        <button class="zeya-areas__toggle" type="button" data-zeya-motion-toggle aria-label="Play video" hidden>
          <svg class="zeya-motion__play" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M4 2.5v11l9.5-5.5z"/></svg>
          <svg class="zeya-motion__pause" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M3.5 2.5h3v11h-3zM9.5 2.5h3v11h-3z"/></svg>
        </button>
      </div>
    </div>
    <div class="zeya-areas__directory"><p>Select your area to enquire</p><span aria-hidden="true"></span></div>
    <ul class="zeya-areas__list"><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Arabian Ranches">Arabian Ranches</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Downtown Dubai">Downtown Dubai</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="JLT">JLT</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="JBR">JBR</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="The Springs">The Springs</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="The Meadows">The Meadows</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="DAMAC Hills">DAMAC Hills</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Al Barsha">Al Barsha</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Mirdif">Mirdif</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Silicon Oasis">Silicon Oasis</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Motor City">Motor City</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Tilal Al Ghaf">Tilal Al Ghaf</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Meydan">Meydan</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Dubai Creek Harbour">Dubai Creek Harbour</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Emirates Hills">Emirates Hills</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Dubai Marina">Dubai Marina</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="DAMAC Hills 1">DAMAC Hills 1</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Town Square">Town Square</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Jumeirah Golf Estates">Jumeirah Golf Estates</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Jumeirah Village Circle (JVC)">Jumeirah Village Circle (JVC)</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Palm Jumeirah">Palm Jumeirah</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Jumeirah Islands">Jumeirah Islands</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Jumeirah Park">Jumeirah Park</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Mira &amp; Mira Oasis">Mira &amp; Mira Oasis</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="The Lakes">The Lakes</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Business Bay">Business Bay</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Dubai Hills">Dubai Hills</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Mudon">Mudon</a></li><li><a class="zeya-areas__chip" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>" data-zeya-wa="area" data-zeya-wa-area="Dubai Sports City">Dubai Sports City</a></li></ul>
  </div>
</section>
<?php
get_footer();
