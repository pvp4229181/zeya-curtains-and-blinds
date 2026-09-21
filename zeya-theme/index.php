<?php
/**
 * Fallback template. ZEYA is a brochure site, so this simply renders whatever
 * the query returned inside the standard page shell.
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
			<h1 class="zeya-pagehead__title">
				<?php
				if ( is_home() || is_front_page() ) {
					bloginfo( 'name' );
				} elseif ( is_search() ) {
					/* translators: %s: search query. */
					printf( esc_html__( 'Search: %s', 'zeya' ), esc_html( get_search_query() ) );
				} else {
					the_archive_title();
				}
				?>
			</h1>
			<span class="zeya-rule"></span>
		</div>
	</div>
</section>

<section class="zeya-section zeya-section--sm">
	<div class="zeya-container">
		<?php if ( have_posts() ) : ?>
			<div class="zeya-stack-lg">
				<?php
				while ( have_posts() ) :
					the_post();
					?>
					<article <?php post_class( 'zeya-reveal' ); ?>>
						<h2 class="zeya-h3">
							<a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
						</h2>
						<div class="zeya-text zeya-mt-sm"><?php the_excerpt(); ?></div>
					</article>
					<?php
				endwhile;
				?>
			</div>
			<div class="zeya-mt"><?php the_posts_pagination(); ?></div>
		<?php else : ?>
			<p class="zeya-text"><?php esc_html_e( 'Nothing found.', 'zeya' ); ?></p>
		<?php endif; ?>
	</div>
</section>

<?php
get_footer();
