<?php
/**
 * Footer: closing band, the cinematic final CTA and the dark footer.
 *
 * @package ZEYA
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

$zeya_images = zeya_asset( 'images/' );
?>
</main>

<section class="zeya-footer-band">
	<div class="zeya-container zeya-footer-band__inner">
		<div class="zeya-reveal">
			<a class="zeya-logo " href="<?php echo esc_url( home_url( '/' ) ); ?>"
			   aria-label="<?php esc_attr_e( 'ZEYA Curtains and Blinds — home', 'zeya' ); ?>">
				<span class="zeya-logo__mark">ZEYA</span>
				<span class="zeya-logo__sub"><?php esc_html_e( 'Curtains &amp; Blinds', 'zeya' ); ?></span>
			</a>
			<p class="zeya-footer-band__tag"><?php esc_html_e( 'Measured. Designed. Installed.', 'zeya' ); ?></p>
		</div>
		<p class="zeya-footer-band__line zeya-reveal">
			<?php esc_html_e( 'Making Spaces', 'zeya' ); ?><br><?php esc_html_e( 'More Beautiful, Together.', 'zeya' ); ?>
		</p>
	</div>
</section>

<section class="zeya-cta">
	<div class="zeya-cta__media" data-zeya-parallax="0.1">
		<img src="<?php echo esc_url( $zeya_images . 'cta-dubai-interior.webp' ); ?>"
		     srcset="<?php echo esc_attr(
			     esc_url( $zeya_images . 'cta-dubai-interior-640.webp' ) . ' 640w, ' .
			     esc_url( $zeya_images . 'cta-dubai-interior-1024.webp' ) . ' 1024w, ' .
			     esc_url( $zeya_images . 'cta-dubai-interior-1600.webp' ) . ' 1600w, ' .
			     esc_url( $zeya_images . 'cta-dubai-interior.webp' ) . ' 2400w'
		     ); ?>"
		     sizes="100vw" width="2400" height="1200" loading="lazy" decoding="async"
		     alt="<?php esc_attr_e( 'Luxury Dubai apartment interior at dusk with full-height curtains framing the city skyline', 'zeya' ); ?>">
	</div>
	<div class="zeya-container zeya-cta__inner">
		<span class="zeya-logo zeya-logo--lg zeya-logo--center zeya-reveal">
			<span class="zeya-logo__mark">ZEYA</span>
			<span class="zeya-logo__sub"><?php esc_html_e( 'Curtains &amp; Blinds', 'zeya' ); ?></span>
		</span>
		<p class="zeya-cta__tag zeya-reveal"><?php esc_html_e( 'Measured. Designed. Installed.', 'zeya' ); ?></p>
		<div class="zeya-cta__actions zeya-reveal">
			<a class="zeya-btn zeya-btn--gold" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>">
				<?php esc_html_e( 'Book a Free Consultation', 'zeya' ); ?>
				<?php zeya_icon( 'arrow-right', 'zeya-btn__arrow' ); ?>
			</a>
		</div>
	</div>
</section>

<footer class="zeya-footer">
	<div class="zeya-container zeya-container--wide zeya-footer__inner">

		<nav class="zeya-footer__nav" aria-label="<?php esc_attr_e( 'Footer', 'zeya' ); ?>">
			<?php
			wp_nav_menu( array(
				'theme_location' => 'footer',
				'container'      => false,
				'items_wrap'     => '%3$s',
				'depth'          => 1,
				'fallback_cb'    => 'zeya_footer_nav_fallback',
			) );
			?>
		</nav>

		<ul class="zeya-footer__contact">
			<li>
				<a data-zeya-contact="address">
					<?php zeya_icon( 'pin' ); ?><span><?php echo esc_html( zeya_contact( 'address', 'Dubai, UAE' ) ); ?></span>
				</a>
			</li>
			<li>
				<a data-zeya-contact="whatsapp">
					<?php zeya_icon( 'whatsapp' ); ?><span><?php esc_html_e( 'WhatsApp', 'zeya' ); ?></span>
				</a>
			</li>
			<li>
				<a data-zeya-contact="phone">
					<?php zeya_icon( 'phone' ); ?><span><?php esc_html_e( 'Phone', 'zeya' ); ?></span>
				</a>
			</li>
			<li>
				<a data-zeya-contact="email">
					<?php zeya_icon( 'mail' ); ?><span><?php esc_html_e( 'Email', 'zeya' ); ?></span>
				</a>
			</li>
		</ul>

		<ul class="zeya-footer__social">
			<li>
				<a class="zeya-social-link" data-zeya-social="instagram"
				   aria-label="<?php esc_attr_e( 'ZEYA on Instagram', 'zeya' ); ?>"><?php zeya_icon( 'instagram' ); ?></a>
			</li>
			<li>
				<a class="zeya-social-link" data-zeya-social="facebook"
				   aria-label="<?php esc_attr_e( 'ZEYA on Facebook', 'zeya' ); ?>"><?php zeya_icon( 'facebook' ); ?></a>
			</li>
			<li>
				<a class="zeya-social-link" data-zeya-social="whatsapp"
				   aria-label="<?php esc_attr_e( 'ZEYA on WhatsApp', 'zeya' ); ?>"><?php zeya_icon( 'whatsapp' ); ?></a>
			</li>
		</ul>

	</div>

	<div class="zeya-container zeya-container--wide zeya-footer__bar">
		<p>
			&copy; <span data-zeya-year><?php echo esc_html( gmdate( 'Y' ) ); ?></span>
			<?php echo esc_html( get_bloginfo( 'name' ) ? get_bloginfo( 'name' ) : 'ZEYA Curtains & Blinds' ); ?>.
			<?php esc_html_e( 'All Rights Reserved.', 'zeya' ); ?>
		</p>
		<p><?php echo esc_html( zeya_contact( 'address', 'Dubai, UAE' ) ); ?></p>
	</div>
</footer>

<?php wp_footer(); ?>
</body>
</html>
