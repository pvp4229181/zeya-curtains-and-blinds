<?php
/**
 * ZEYA Curtains & Blinds — theme functions.
 *
 * @package ZEYA
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'ZEYA_VERSION', '1.0.0' );

/**
 * ---------------------------------------------------------------------------
 * CONTACT DETAILS
 * ---------------------------------------------------------------------------
 * The single place ZEYA's real contact details are configured. Everything is
 * empty by default: an empty value renders as a plain, unlinked label, so the
 * site never shows an invented phone number, WhatsApp number or address.
 *
 * Edit the defaults below, set them under Appearance → Customize → ZEYA
 * Contact Details, or override them with the `zeya_contact_details` filter.
 */
function zeya_contact_details() {
	$defaults = array(
		'address'       => 'Dubai, UAE',
		'addressLine'   => '', // Optional second line, e.g. a street address.
		'addressUrl'    => '', // e.g. a Google Maps link.
		'whatsapp'      => '', // Digits only, e.g. 971500000000.
		'whatsappLabel' => '', // Display form, e.g. +971 50 000 0000.
		'phone'         => '',
		'email'         => '',
		'instagram'     => '', // Full profile URL.
		'facebook'      => '', // Full profile URL.
		'formEndpoint'  => '', // POST target; leave empty until a handler exists.
	);

	// Customizer values take precedence over the defaults above.
	$mods = array(
		'address'       => 'zeya_address',
		'addressLine'   => 'zeya_address_line',
		'addressUrl'    => 'zeya_address_url',
		'whatsapp'      => 'zeya_whatsapp',
		'whatsappLabel' => 'zeya_whatsapp_label',
		'phone'         => 'zeya_phone',
		'email'         => 'zeya_email',
		'instagram'     => 'zeya_instagram',
		'facebook'      => 'zeya_facebook',
		'formEndpoint'  => 'zeya_form_endpoint',
	);

	$details = $defaults;
	foreach ( $mods as $key => $mod ) {
		$value = get_theme_mod( $mod, '' );
		if ( '' !== $value && null !== $value ) {
			$details[ $key ] = $value;
		}
	}

	/**
	 * Filter the ZEYA contact details.
	 *
	 * @param array $details Contact details keyed as above.
	 */
	return apply_filters( 'zeya_contact_details', $details );
}

/**
 * Return a single contact detail, sanitised for output.
 *
 * @param string $key     Detail key.
 * @param string $default Fallback.
 * @return string
 */
function zeya_contact( $key, $default = '' ) {
	$details = zeya_contact_details();
	return isset( $details[ $key ] ) && '' !== $details[ $key ] ? $details[ $key ] : $default;
}

/**
 * ---------------------------------------------------------------------------
 * Theme setup
 * ---------------------------------------------------------------------------
 */
function zeya_setup() {
	load_theme_textdomain( 'zeya', get_template_directory() . '/languages' );

	add_theme_support( 'title-tag' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'automatic-feed-links' );
	add_theme_support( 'responsive-embeds' );
	add_theme_support( 'custom-logo', array(
		'height'      => 48,
		'width'       => 180,
		'flex-height' => true,
		'flex-width'  => true,
	) );
	add_theme_support( 'html5', array(
		'search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'style', 'script',
	) );

	register_nav_menus( array(
		'primary' => __( 'Primary Navigation', 'zeya' ),
		'footer'  => __( 'Footer Navigation', 'zeya' ),
	) );
}
add_action( 'after_setup_theme', 'zeya_setup' );

/**
 * ---------------------------------------------------------------------------
 * Assets — enqueued here, never inlined in the page templates.
 * ---------------------------------------------------------------------------
 */
function zeya_enqueue_assets() {
	$uri = get_template_directory_uri();
	$dir = get_template_directory();

	// Fonts. Cormorant Garamond for display, Inter for UI.
	wp_enqueue_style(
		'zeya-fonts',
		'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500&family=Inter:wght@300;400;500;600&display=swap',
		array(),
		null
	);

	$sheets = array(
		'zeya-style'      => 'assets/css/style.css',
		'zeya-animations' => 'assets/css/animations.css',
		'zeya-responsive' => 'assets/css/responsive.css',
	);

	$previous = 'zeya-fonts';
	foreach ( $sheets as $handle => $path ) {
		wp_enqueue_style(
			$handle,
			$uri . '/' . $path,
			array( $previous ),
			file_exists( $dir . '/' . $path ) ? filemtime( $dir . '/' . $path ) : ZEYA_VERSION
		);
		$previous = $handle;
	}

	// The theme's own style.css carries the theme header; keep it last so child
	// themes and user tweaks win.
	wp_enqueue_style( 'zeya-theme', get_stylesheet_uri(), array( $previous ), ZEYA_VERSION );

	$scripts = array(
		'zeya-main'          => 'assets/js/main.js',
		'zeya-animations-js' => 'assets/js/animations.js',
	);

	foreach ( $scripts as $handle => $path ) {
		wp_enqueue_script(
			$handle,
			$uri . '/' . $path,
			array(),
			file_exists( $dir . '/' . $path ) ? filemtime( $dir . '/' . $path ) : ZEYA_VERSION,
			array( 'strategy' => 'defer', 'in_footer' => true )
		);
	}

	// Hand the contact configuration to the front end.
	wp_localize_script( 'zeya-main', 'ZEYA_CONTACT', zeya_contact_details() );
}
add_action( 'wp_enqueue_scripts', 'zeya_enqueue_assets' );

/**
 * Preload the hero image on the front page so the LCP element is discovered
 * early. It is the only image that is not lazy-loaded.
 */
function zeya_preload_hero() {
	if ( ! is_front_page() ) {
		return;
	}
	$uri = get_template_directory_uri() . '/assets/images/';
	printf(
		'<link rel="preload" as="image" href="%1$s" imagesrcset="%2$s" imagesizes="100vw" fetchpriority="high">' . "\n",
		esc_url( $uri . 'hero-luxury-curtains-1600.webp' ),
		esc_attr(
			esc_url( $uri . 'hero-luxury-curtains-1024.webp' ) . ' 1024w, ' .
			esc_url( $uri . 'hero-luxury-curtains-1600.webp' ) . ' 1600w, ' .
			esc_url( $uri . 'hero-luxury-curtains.webp' ) . ' 2400w'
		)
	);
}
add_action( 'wp_head', 'zeya_preload_hero', 2 );

/**
 * ---------------------------------------------------------------------------
 * Helpers used by the templates
 * ---------------------------------------------------------------------------
 */

/**
 * URL of a theme asset.
 *
 * @param string $path Path below assets/, e.g. "images/hero.webp".
 * @return string
 */
function zeya_asset( $path ) {
	return get_template_directory_uri() . '/assets/' . ltrim( $path, '/' );
}

/**
 * Permalink for one of the site's main pages, by slug.
 *
 * Falls back to the home URL so the navigation never produces a dead link on a
 * fresh install where the pages have not been created yet.
 *
 * @param string $slug Page slug: home, about, products, process, contact.
 * @return string
 */
function zeya_link( $slug ) {
	if ( 'home' === $slug ) {
		return home_url( '/' );
	}

	$page = get_page_by_path( $slug );
	if ( $page instanceof WP_Post ) {
		return get_permalink( $page );
	}

	return home_url( '/' . $slug . '/' );
}

/**
 * The current page's ZEYA slug, used for the active-navigation indicator.
 *
 * @return string
 */
function zeya_current_page() {
	if ( is_front_page() ) {
		return 'home';
	}

	$post = get_queried_object();
	if ( $post instanceof WP_Post && in_array( $post->post_name, array( 'about', 'products', 'process', 'contact' ), true ) ) {
		return $post->post_name;
	}

	return '';
}

/**
 * Print the inline icon sprite once per page.
 */
function zeya_icon_sprite() {
	require get_template_directory() . '/inc/icons.php';
}

/**
 * Render one icon from the sprite.
 *
 * @param string $name  Icon name without the `zeya-i-` prefix.
 * @param string $class Optional CSS class.
 */
function zeya_icon( $name, $class = '' ) {
	printf(
		'<svg%1$s aria-hidden="true" focusable="false"><use href="#zeya-i-%2$s"></use></svg>',
		$class ? ' class="' . esc_attr( $class ) . '"' : '',
		esc_attr( $name )
	);
}

/**
 * ---------------------------------------------------------------------------
 * Navigation integration
 * ---------------------------------------------------------------------------
 */

/**
 * Add the theme's link class and the active-state hook to menu links.
 *
 * @param array   $atts Link attributes.
 * @param WP_Post $item Menu item.
 * @return array
 */
function zeya_nav_link_attributes( $atts, $item ) {
	$atts['class'] = trim( ( isset( $atts['class'] ) ? $atts['class'] : '' ) . ' zeya-nav__link' );

	// Match the JS active-page indicator to the linked page's slug.
	if ( ! empty( $item->object_id ) && 'page' === $item->object ) {
		$linked = get_post( $item->object_id );
		if ( $linked instanceof WP_Post ) {
			$slug = ( (int) get_option( 'page_on_front' ) === (int) $linked->ID ) ? 'home' : $linked->post_name;
			$atts['data-zeya-nav-item'] = $slug;
		}
	}

	return $atts;
}
add_filter( 'nav_menu_link_attributes', 'zeya_nav_link_attributes', 10, 2 );

/**
 * Fallback primary navigation, used until a menu is assigned in the admin.
 */
function zeya_primary_nav_fallback() {
	$items = array(
		'home'     => __( 'Home', 'zeya' ),
		'about'    => __( 'About', 'zeya' ),
		'products' => __( 'Products', 'zeya' ),
		'process'  => __( 'Process', 'zeya' ),
		'contact'  => __( 'Contact', 'zeya' ),
	);

	echo '<ul class="zeya-nav__list">';
	foreach ( $items as $slug => $label ) {
		printf(
			'<li><a class="zeya-nav__link" data-zeya-nav-item="%1$s" href="%2$s">%3$s</a></li>',
			esc_attr( $slug ),
			esc_url( zeya_link( $slug ) ),
			esc_html( $label )
		);
	}
	echo '</ul>';
}

/**
 * Fallback footer navigation.
 */
function zeya_footer_nav_fallback() {
	$items = array(
		'home'     => __( 'Home', 'zeya' ),
		'about'    => __( 'About', 'zeya' ),
		'products' => __( 'Products', 'zeya' ),
		'process'  => __( 'Process', 'zeya' ),
		'contact'  => __( 'Contact', 'zeya' ),
	);

	foreach ( $items as $slug => $label ) {
		printf(
			'<a class="zeya-footer__link" href="%1$s">%2$s</a>',
			esc_url( zeya_link( $slug ) ),
			esc_html( $label )
		);
	}
}

/**
 * Add the page identifier to the body classes.
 *
 * @param array $classes Body classes.
 * @return array
 */
function zeya_body_class( $classes ) {
	$classes[] = 'zeya-body';
	$page      = zeya_current_page();
	if ( $page ) {
		$classes[] = 'zeya-page--' . $page;
	}
	return $classes;
}
add_filter( 'body_class', 'zeya_body_class' );

/**
 * ---------------------------------------------------------------------------
 * Customizer — ZEYA contact details
 * ---------------------------------------------------------------------------
 */
function zeya_customize_register( $wp_customize ) {
	$wp_customize->add_section( 'zeya_contact', array(
		'title'       => __( 'ZEYA Contact Details', 'zeya' ),
		'priority'    => 30,
		'description' => __( 'Leave a field empty to show the label only, with no link. Nothing is invented for you.', 'zeya' ),
	) );

	$fields = array(
		'zeya_address'        => array( __( 'Location label', 'zeya' ), 'Dubai, UAE', 'sanitize_text_field' ),
		'zeya_address_line'   => array( __( 'Address (second line)', 'zeya' ), '', 'sanitize_text_field' ),
		'zeya_address_url'    => array( __( 'Map link', 'zeya' ), '', 'esc_url_raw' ),
		'zeya_whatsapp'       => array( __( 'WhatsApp number (digits only)', 'zeya' ), '', 'sanitize_text_field' ),
		'zeya_whatsapp_label' => array( __( 'WhatsApp number (display form)', 'zeya' ), '', 'sanitize_text_field' ),
		'zeya_phone'          => array( __( 'Phone number', 'zeya' ), '', 'sanitize_text_field' ),
		'zeya_email'          => array( __( 'Email address', 'zeya' ), '', 'sanitize_email' ),
		'zeya_instagram'      => array( __( 'Instagram URL', 'zeya' ), '', 'esc_url_raw' ),
		'zeya_facebook'       => array( __( 'Facebook URL', 'zeya' ), '', 'esc_url_raw' ),
		'zeya_form_endpoint'  => array( __( 'Contact form endpoint', 'zeya' ), '', 'esc_url_raw' ),
	);

	foreach ( $fields as $id => $field ) {
		list( $label, $default, $sanitize ) = $field;

		$wp_customize->add_setting( $id, array(
			'default'           => $default,
			'sanitize_callback' => $sanitize,
			'transport'         => 'refresh',
		) );

		$wp_customize->add_control( $id, array(
			'label'   => $label,
			'section' => 'zeya_contact',
			'type'    => 'text',
		) );
	}
}
add_action( 'customize_register', 'zeya_customize_register' );

/**
 * ---------------------------------------------------------------------------
 * Contact form
 * ---------------------------------------------------------------------------
 * If Contact Form 7 or WPForms is active and an ID has been configured, the
 * plugin renders the form. Otherwise the theme's own accessible markup is used,
 * which validates in the browser but does not claim to send anything until an
 * endpoint is configured.
 *
 * Set the shortcode with:
 *   add_filter( 'zeya_contact_form_shortcode', function () {
 *       return '[contact-form-7 id="123" title="ZEYA enquiry"]';
 *   } );
 */
function zeya_contact_form_shortcode() {
	return apply_filters( 'zeya_contact_form_shortcode', '' );
}

/**
 * Whether a form plugin is handling the contact form.
 *
 * @return bool
 */
function zeya_has_form_plugin() {
	return '' !== trim( zeya_contact_form_shortcode() );
}
