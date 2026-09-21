<?php
/**
 * 404 template.
 *
 * @package ZEYA
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();
?>

<section class="zeya-pagehead">
	<div class="zeya-container zeya-pagehead__grid">
		<div class="zeya-pagehead__left zeya-reveal">
			<h1 class="zeya-pagehead__title"><?php esc_html_e( 'Page Not Found', 'zeya' ); ?></h1>
			<span class="zeya-rule"></span>
		</div>
		<div class="zeya-pagehead__right zeya-reveal">
			<h2 class="zeya-pagehead__lead"><?php esc_html_e( 'Let us point you back to the window.', 'zeya' ); ?></h2>
			<p class="zeya-pagehead__text">
				<?php esc_html_e( 'The page you were looking for is not here. Browse our curtains, blinds and motorized solutions, or book a free consultation.', 'zeya' ); ?>
			</p>
			<p class="zeya-mt-sm">
				<a class="zeya-btn zeya-btn--gold" href="<?php echo esc_url( zeya_link( 'products' ) ); ?>">
					<?php esc_html_e( 'Explore Our Products', 'zeya' ); ?>
					<?php zeya_icon( 'arrow-right', 'zeya-btn__arrow' ); ?>
				</a>
			</p>
		</div>
	</div>
</section>

<?php
get_footer();
