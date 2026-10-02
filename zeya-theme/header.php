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

// The top strip starts from the configured details; main.js re-applies the
// same values, like the footer rows. The number falls back to WhatsApp.
$zeya_contact = zeya_contact_details();
$zeya_call    = $zeya_contact['phone'] ? $zeya_contact['phone'] : $zeya_contact['whatsappLabel'];
$zeya_studio  = $zeya_contact['addressLine'] ? $zeya_contact['addressLine'] : $zeya_contact['address'];
?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#171411">
<link rel="profile" href="https://gmpg.org/xfn/11">
<link rel="icon" href="<?php echo esc_url( zeya_asset( 'icons/favicon.ico?v=4' ) ); ?>" sizes="32x32">
<link rel="icon" href="<?php echo esc_url( zeya_asset( 'icons/favicon-32.png?v=4' ) ); ?>" type="image/png" sizes="32x32">
<link rel="icon" href="<?php echo esc_url( zeya_asset( 'icons/favicon-192.png?v=4' ) ); ?>" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="<?php echo esc_url( zeya_asset( 'icons/apple-touch-icon.png?v=4' ) ); ?>">
<script>document.documentElement.classList.add('zeya-js');</script>
<?php wp_head(); ?>
</head>

<body <?php body_class(); ?><?php echo $zeya_page ? ' data-zeya-page="' . esc_attr( $zeya_page ) . '"' : ''; ?>>
<?php wp_body_open(); ?>

<a class="zeya-skip" href="#zeya-main"><?php esc_html_e( 'Skip to content', 'zeya' ); ?></a>

<?php zeya_icon_sprite(); ?>

<?php $zeya_images = zeya_asset( 'images/' ); ?>
<div class="zeya-topbar" data-zeya-topbar><div class="zeya-container zeya-container--wide zeya-topbar__inner"><div class="zeya-topbar__info"><span class="zeya-topbar__item" data-zeya-contact="hours"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-clock"></use></svg><span data-zeya-contact-value>Monday &ndash; Saturday 9:00 &ndash; 18:00</span></span><a class="zeya-topbar__item" data-zeya-contact="call"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-phone"></use></svg><span data-zeya-contact-value>+971 50 000 0000</span></a><a class="zeya-topbar__item" data-zeya-contact="address"><svg aria-hidden="true" focusable="false"><use href="#zeya-i-pin"></use></svg><span data-zeya-contact-value>Dubai, UAE</span></a></div></div></div>
<header class="zeya-header" data-zeya-header>
  <div class="zeya-container zeya-container--wide zeya-header__inner">
    <a class="zeya-logo " href="<?php echo esc_url( zeya_link( 'home' ) ); ?>" aria-label="ZEYA Curtains and Blinds — home"><img class="zeya-logo__img" src="<?php echo esc_url( zeya_asset( 'images/zeya.png' ) ); ?>" sizes="(max-width: 640px) 200px, 330px" width="1600" height="800" alt="ZEYA Curtains &amp; Blinds" loading="eager" fetchpriority="high" decoding="async"></a>
    <nav class="zeya-nav" id="zeya-nav" data-zeya-nav aria-label="Primary">
      <ul class="zeya-nav__list"><li><a class="zeya-nav__link" data-zeya-nav-item="home" href="<?php echo esc_url( zeya_link( 'home' ) ); ?>">Home</a></li><li class="zeya-nav-products"><a class="zeya-nav__link" data-zeya-nav-item="products" href="<?php echo esc_url( zeya_link( 'products' ) ); ?>">Collections</a><details class="zeya-product-menu"><summary>Browse collections<svg aria-hidden="true" focusable="false"><use href="#zeya-i-arrow-right"></use></svg></summary><div class="zeya-product-menu__panel"><div class="zeya-menu-columns"><div class="zeya-menu-categories"><button type="button" class="zeya-menu-category" data-zeya-menu-category="curtains" aria-controls="zeya-menu-curtains" aria-expanded="true">Curtains<span aria-hidden="true">&#8250;</span></button><button type="button" class="zeya-menu-category" data-zeya-menu-category="blinds" aria-controls="zeya-menu-blinds" aria-expanded="false">Blinds<span aria-hidden="true">&#8250;</span></button><button type="button" class="zeya-menu-category" data-zeya-menu-category="motorized" aria-controls="zeya-menu-motorized" aria-expanded="false">Motorized Solutions<span aria-hidden="true">&#8250;</span></button><button type="button" class="zeya-menu-category" data-zeya-menu-category="curtain-accessories" aria-controls="zeya-menu-curtain-accessories" aria-expanded="false">Accessories<span aria-hidden="true">&#8250;</span></button></div><div class="zeya-menu-products-wrap"><div class="zeya-menu-products" id="zeya-menu-curtains"><a class="zeya-menu-all" href="<?php echo esc_url( zeya_link( 'curtains' ) ); ?>">View all curtains</a><a href="<?php echo esc_url( zeya_link( 'product-sheer-curtains' ) ); ?>">Sheer Curtains</a><a href="<?php echo esc_url( zeya_link( 'product-blackout-curtains' ) ); ?>">Blackout Curtains</a><a href="<?php echo esc_url( zeya_link( 'product-linen-curtains' ) ); ?>">Linen Curtains</a><a href="<?php echo esc_url( zeya_link( 'product-velvet-curtains' ) ); ?>">Velvet Curtains</a><a href="<?php echo esc_url( zeya_link( 'product-wave-curtains' ) ); ?>">Wave Curtains</a><a href="<?php echo esc_url( zeya_link( 'product-pinch-pleat-curtains' ) ); ?>">Pinch Pleat Curtains</a><a href="<?php echo esc_url( zeya_link( 'product-double-layered-curtains' ) ); ?>">Double / Layered Curtains</a><a href="<?php echo esc_url( zeya_link( 'product-motorized-curtains' ) ); ?>">Motorized Curtains</a></div><div class="zeya-menu-products" id="zeya-menu-blinds" hidden><a class="zeya-menu-all" href="<?php echo esc_url( zeya_link( 'blinds' ) ); ?>">View all blinds</a><a href="<?php echo esc_url( zeya_link( 'product-roller-blinds' ) ); ?>">Roller Blinds</a><a href="<?php echo esc_url( zeya_link( 'product-zebra-blinds' ) ); ?>">Zebra Blinds</a><a href="<?php echo esc_url( zeya_link( 'product-roman-blinds' ) ); ?>">Roman Blinds</a><a href="<?php echo esc_url( zeya_link( 'product-venetian-blinds' ) ); ?>">Venetian Blinds</a><a href="<?php echo esc_url( zeya_link( 'product-wooden-blinds' ) ); ?>">Wooden Blinds</a><a href="<?php echo esc_url( zeya_link( 'product-faux-wood-blinds' ) ); ?>">Faux Wood Blinds</a><a href="<?php echo esc_url( zeya_link( 'product-vertical-blinds' ) ); ?>">Vertical Blinds</a><a href="<?php echo esc_url( zeya_link( 'product-honeycomb-blinds' ) ); ?>">Honeycomb Blinds</a><a href="<?php echo esc_url( zeya_link( 'product-sunscreen-blinds' ) ); ?>">Sunscreen Blinds</a><a href="<?php echo esc_url( zeya_link( 'product-motorized-blinds' ) ); ?>">Motorized Blinds</a></div><div class="zeya-menu-products" id="zeya-menu-motorized" hidden><a class="zeya-menu-all" href="<?php echo esc_url( zeya_link( 'motorized' ) ); ?>">View all motorized solutions</a><a href="<?php echo esc_url( zeya_link( 'product-motorized-curtains' ) ); ?>">Motorized Curtains</a><a href="<?php echo esc_url( zeya_link( 'product-motorized-blinds' ) ); ?>">Motorized Blinds</a><a href="<?php echo esc_url( zeya_link( 'product-motorized-curtain-tracks' ) ); ?>">Motorized Curtain Tracks</a><a href="<?php echo esc_url( zeya_link( 'product-motorized-roller-blinds' ) ); ?>">Motorized Roller Blinds</a><a href="<?php echo esc_url( zeya_link( 'product-motorized-roman-blinds' ) ); ?>">Motorized Roman Blinds</a><a href="<?php echo esc_url( zeya_link( 'product-motorized-zebra-blinds' ) ); ?>">Motorized Zebra Blinds</a><a href="<?php echo esc_url( zeya_link( 'product-smart-window-automation' ) ); ?>">Smart Window Automation</a></div><div class="zeya-menu-products" id="zeya-menu-curtain-accessories" hidden><a class="zeya-menu-all" href="<?php echo esc_url( zeya_link( 'curtain-accessories' ) ); ?>">View all accessories</a><a href="<?php echo esc_url( zeya_link( 'product-curtain-rods-poles' ) ); ?>">Curtain Rods &amp; Poles</a><a href="<?php echo esc_url( zeya_link( 'product-curtain-tracks' ) ); ?>">Curtain Tracks</a><a href="<?php echo esc_url( zeya_link( 'product-curtain-rings-hooks' ) ); ?>">Curtain Rings &amp; Hooks</a><a href="<?php echo esc_url( zeya_link( 'product-finials-end-caps' ) ); ?>">Finials &amp; End Caps</a><a href="<?php echo esc_url( zeya_link( 'product-tiebacks-holdbacks' ) ); ?>">Tiebacks &amp; Holdbacks</a><a href="<?php echo esc_url( zeya_link( 'product-pelmets-valances' ) ); ?>">Pelmets &amp; Valances</a><a href="<?php echo esc_url( zeya_link( 'product-curtain-linings' ) ); ?>">Curtain Linings</a><a href="<?php echo esc_url( zeya_link( 'product-motorized-accessories' ) ); ?>">Motorized Accessories</a></div></div></div><div class="zeya-product-menu__foot"><a href="<?php echo esc_url( zeya_link( 'products' ) ); ?>">View all collections</a><a href="<?php echo esc_url( zeya_link( 'residential-commercial' ) ); ?>">Homes &amp; workplaces</a></div></div></details></li><li><a class="zeya-nav__link" data-zeya-nav-item="about" href="<?php echo esc_url( zeya_link( 'about' ) ); ?>">About Us</a></li><li><a class="zeya-nav__link" data-zeya-nav-item="process" href="<?php echo esc_url( zeya_link( 'process' ) ); ?>">Our Process</a></li><li><a class="zeya-nav__link" data-zeya-nav-item="faq" href="<?php echo esc_url( zeya_link( 'faq' ) ); ?>">FAQs</a></li><li><a class="zeya-nav__link" data-zeya-nav-item="contact" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>">Contact</a></li></ul>
      <a class="zeya-btn zeya-btn--line zeya-nav__cta" href="<?php echo esc_url( zeya_link( 'contact' ) ); ?>">Book a Free Consultation <span aria-hidden="true">&#8594;</span></a>
    </nav>
    <button class="zeya-burger" type="button" data-zeya-burger
            aria-expanded="false" aria-controls="zeya-nav" aria-label="Open menu">
      <span class="zeya-burger__bar"></span>
      <span class="zeya-burger__bar"></span>
      <span class="zeya-burger__bar"></span>
    </button>
  </div>
</header>

<main id="zeya-main">
