<?php
/**
 * Header: document head, icon sprite and the sticky primary navigation.
 *
 * @package ZEYA
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// Every page now opens on a full-bleed hero, so the bar always starts
// transparent and main.js swaps it to the solid shell once the hero has
// scrolled away. The solid modifier stays available for templates without one.
$zeya_solid = apply_filters( 'zeya_header_solid', false ) ? ' zeya-header--solid' : '';
$zeya_page  = zeya_current_page();
?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#191713">
<link rel="profile" href="https://gmpg.org/xfn/11">
<link rel="icon" href="<?php echo esc_url( zeya_asset( 'icons/favicon.ico' ) ); ?>" sizes="32x32">
<link rel="icon" href="<?php echo esc_url( zeya_asset( 'icons/favicon-32.png' ) ); ?>" type="image/png" sizes="32x32">
<link rel="icon" href="<?php echo esc_url( zeya_asset( 'icons/favicon-192.png' ) ); ?>" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="<?php echo esc_url( zeya_asset( 'icons/apple-touch-icon.png' ) ); ?>">
<script>document.documentElement.classList.add('zeya-js');</script>
<?php wp_head(); ?>
</head>

<body <?php body_class(); ?><?php echo $zeya_page ? ' data-zeya-page="' . esc_attr( $zeya_page ) . '"' : ''; ?>>
<?php wp_body_open(); ?>

<a class="zeya-skip" href="#zeya-main"><?php esc_html_e( 'Skip to content', 'zeya' ); ?></a>

<?php zeya_icon_sprite(); ?>

<header class="zeya-header<?php echo esc_attr( $zeya_solid ); ?>" data-zeya-header>
	<div class="zeya-container zeya-container--wide zeya-header__inner">

		<?php if ( has_custom_logo() ) : ?>
			<?php the_custom_logo(); ?>
		<?php else : ?>
			<a class="zeya-logo " href="<?php echo esc_url( home_url( '/' ) ); ?>"
			   aria-label="<?php esc_attr_e( 'ZEYA Curtains and Blinds — home', 'zeya' ); ?>">
				<img class="zeya-logo__img"
				     src="<?php echo esc_url( zeya_asset( 'images/zeya-logo-footer.webp' ) ); ?>"
				     srcset="<?php echo esc_attr(
					     esc_url( zeya_asset( 'images/zeya-logo-footer-360.webp' ) ) . ' 360w, ' .
					     esc_url( zeya_asset( 'images/zeya-logo-footer.webp' ) ) . ' 720w'
				     ); ?>"
				     sizes="(max-width: 640px) 180px, 260px" width="720" height="238"
				     loading="eager" fetchpriority="high" decoding="async"
				     alt="<?php esc_attr_e( 'ZEYA Curtains &amp; Blinds', 'zeya' ); ?>">
			</a>
		<?php endif; ?>

		<nav class="zeya-nav" id="zeya-nav" data-zeya-nav aria-label="<?php esc_attr_e( 'Primary', 'zeya' ); ?>">
			<?php
			wp_nav_menu( array(
				'theme_location' => 'primary',
				'container'      => false,
				'menu_class'     => 'zeya-nav__list',
				'depth'          => 1,
				'fallback_cb'    => 'zeya_primary_nav_fallback',
			) );
			?>
			<a class="zeya-btn zeya-btn--line zeya-nav__cta" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>">
				<?php esc_html_e( 'Let’s talk', 'zeya' ); ?>
			</a>
		</nav>

		<button class="zeya-burger" type="button" data-zeya-burger
		        aria-expanded="false" aria-controls="zeya-nav"
		        aria-label="<?php esc_attr_e( 'Open menu', 'zeya' ); ?>">
			<span class="zeya-burger__bar"></span>
			<span class="zeya-burger__bar"></span>
			<span class="zeya-burger__bar"></span>
		</button>

	</div>
</header>

<main id="zeya-main">
