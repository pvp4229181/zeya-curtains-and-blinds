<?php
/**
 * Generic page template, used for any page that does not have a dedicated
 * ZEYA template (page-about.php, page-products.php, …).
 *
 * @package ZEYA
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

while ( have_posts() ) :
	the_post();
	?>

	<section class="zeya-pagehead">
		<div class="zeya-container zeya-pagehead__grid">
			<div class="zeya-pagehead__left zeya-reveal">
				<h1 class="zeya-pagehead__title"><?php the_title(); ?></h1>
				<span class="zeya-rule"></span>
				<nav class="zeya-crumbs" aria-label="<?php esc_attr_e( 'Breadcrumb', 'zeya' ); ?>">
					<a href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php esc_html_e( 'Home', 'zeya' ); ?></a>
					<span class="zeya-crumbs__sep" aria-hidden="true">/</span>
					<span aria-current="page"><?php the_title(); ?></span>
				</nav>
			</div>
		</div>
	</section>

	<section class="zeya-section zeya-section--sm">
		<div class="zeya-container">
			<div class="zeya-text zeya-reveal"><?php the_content(); ?></div>
		</div>
	</section>

	<?php
endwhile;

get_footer();
