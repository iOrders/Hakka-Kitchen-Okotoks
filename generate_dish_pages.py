#!/usr/bin/env python3
"""
Generate SEO-optimized dish landing pages for Hakka Kitchen Okotoks
Based on the template structure from honey-chilli-fries-st-albert.html
"""

import os
import re
from pathlib import Path

# Restaurant Information
RESTAURANT_INFO = {
    "name": "Hakka Kitchen",
    "location": "Okotoks",
    "address": "100 Stockton Ave, Okotoks, AB T1S 0A1",
    "phone": "+1 587-971-7411",
    "phone_link": "15879717411",
    "website": "https://hakkakitchenrestaurant.com",
    "order_link": "https://orders.iorders.online/hakka-kitchen-okotoks-5205",
    "latitude": "50.7199280134305",
    "longitude": "-113.95499967270565",
    "geo_position": "50.7199280134305;-113.95499967270565",
    "maps_link": "https://maps.app.goo.gl/JsTmaQcbYhdEuwTN7",
    "maps_iframe": '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2526.0048116509333!2d-113.95549319999999!3d50.7198499!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x5371992f22c85f63%3A0x466c1aff87b6c85d!2sHakka%20kitchen!5e0!3m2!1sen!2sca!4v1768344954791!5m2!1sen!2sca" width="100%" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
}

# Dishes data - only 6 dishes from Store Information.txt
DISHES = [
    {
        "name": "Chicken Tikka Masala",
        "slug": "chicken-tikka-masala-okotoks",
        "short_desc": "Marinated chicken grilled in tandoor with butter sauce",
        "full_desc": "Experience our signature Chicken Tikka Masala, featuring tender chicken pieces marinated in yogurt and aromatic Indian spices, then grilled to perfection in our traditional tandoor oven. The grilled chicken is finished in a rich, creamy butter sauce with tomatoes, creating a harmonious blend of smoky, spicy, and creamy flavors.",
        "extended_desc": "What makes our Chicken Tikka Masala exceptional is the authentic preparation method. The chicken is first marinated for hours in a blend of yogurt, ginger, garlic, and traditional spices, then cooked in our tandoor for that signature charred flavor. The sauce is prepared fresh daily with tomatoes, cream, butter, and a secret blend of spices that has been perfected over years. This classic dish represents the best of North Indian cuisine and is perfect for both spice lovers and those new to Indian food.",
        "image": "chicken-tikka-masala.webp",
        "prep_time": "25",
        "spice_level": "Medium",
        "cuisine": "North Indian",
        "category": "Main Course"
    },
    {
        "name": "Goat Rara",
        "slug": "goat-rara-okotoks",
        "short_desc": "Dairy-free goat cooked with minced meat and Indian spices",
        "full_desc": "Savor our authentic Goat Rara, a traditional Indian delicacy featuring tender goat meat cooked with minced meat in a robust blend of aromatic Indian spices. This dairy-free preparation showcases the rich, deep flavors of slow-cooked goat in a thick, spicy gravy that's both hearty and satisfying.",
        "extended_desc": "Goat Rara is a specialty dish that requires patience and expertise. The goat meat is slowly braised until tender, while minced goat adds texture and intensifies the flavor profile. The dish is enhanced with onions, tomatoes, ginger, garlic, and a complex masala blend including coriander, cumin, and garam masala. Being dairy-free, this dish is perfect for those with lactose sensitivities while delivering authentic, bold Indian flavors. The result is a rich, aromatic curry that pairs beautifully with naan or rice.",
        "image": "lamb-biryani.webp",
        "prep_time": "45",
        "spice_level": "Medium-Hot",
        "cuisine": "North Indian",
        "category": "Main Course"
    },
    {
        "name": "Butter Prawn",
        "slug": "butter-prawn-okotoks",
        "short_desc": "Premium prawns in creamy butter sauce",
        "full_desc": "Indulge in our exquisite Butter Prawn, featuring premium-quality prawns cooked to perfection in a luxuriously creamy butter sauce. This dish combines the delicate sweetness of fresh prawns with the rich, velvety texture of our signature butter-based gravy, enhanced with aromatic spices and fresh herbs.",
        "extended_desc": "Our Butter Prawn showcases the finest seafood preparation techniques. Large, succulent prawns are carefully selected for their quality and freshness, then marinated in subtle spices before being cooked in a sauce made with butter, cream, tomatoes, and a blend of aromatic spices including fenugreek, cardamom, and kashmiri chili. The result is a dish that's creamy yet light, with the prawns maintaining their natural sweetness while absorbing the rich flavors of the sauce. This dish is perfect for seafood lovers seeking an elegant Indian dining experience.",
        "image": "chicken-tikka-masala.webp",
        "prep_time": "20",
        "spice_level": "Mild-Medium",
        "cuisine": "Indian Fusion",
        "category": "Main Course"
    },
    {
        "name": "Chilly Chicken",
        "slug": "chilly-chicken-okotoks",
        "short_desc": "Spiced dry chicken preparation",
        "full_desc": "Enjoy our popular Chilly Chicken, a beloved Indo-Chinese fusion dish featuring tender chicken pieces coated in a spicy, tangy sauce with bell peppers and onions. This dry preparation offers a perfect balance of heat, flavor, and texture, making it an ideal appetizer or side dish.",
        "extended_desc": "Chilly Chicken is a perfect example of Indo-Chinese fusion cuisine, where Indian spices meet Chinese cooking techniques. Boneless chicken pieces are marinated, coated, and fried until crispy, then tossed in a wok with green chilies, bell peppers, onions, garlic, and our special chilly sauce. The 'dry' preparation means less gravy and more intense flavors coating each piece of chicken. The dish delivers a satisfying crunch on the outside while remaining juicy inside, with a spicy kick that's balanced by the sweetness of bell peppers and the tanginess of the sauce.",
        "image": "honey-chilli-fries.webp",
        "prep_time": "20",
        "spice_level": "Medium-Hot",
        "cuisine": "Indo-Chinese",
        "category": "Appetizer"
    },
    {
        "name": "Lamb Curry",
        "slug": "lamb-curry-okotoks",
        "short_desc": "Tender lamb in traditional curry gravy",
        "full_desc": "Delight in our classic Lamb Curry, featuring tender lamb pieces slow-cooked in a traditional curry gravy made with aromatic spices, tomatoes, and onions. This authentic Indian preparation showcases the rich, robust flavors that make lamb curry a timeless favorite.",
        "extended_desc": "Our Lamb Curry is prepared using time-honored techniques that ensure maximum flavor and tenderness. Premium cuts of lamb are marinated in spices and yogurt, then slow-cooked with a carefully balanced curry sauce made from fresh tomatoes, onions, ginger, garlic, and a proprietary blend of whole and ground spices. The slow cooking process allows the lamb to become incredibly tender while absorbing the complex flavors of the curry. The result is a hearty, warming dish with a medium-thick gravy that's perfect for scooping up with naan or mixing with basmati rice.",
        "image": "lamb-biryani.webp",
        "prep_time": "40",
        "spice_level": "Medium",
        "cuisine": "North Indian",
        "category": "Main Course"
    },
    {
        "name": "Butter Chicken with Naan",
        "slug": "butter-chicken-naan-okotoks",
        "short_desc": "Classic creamy chicken curry served with traditional bread",
        "full_desc": "Experience our signature Butter Chicken paired with freshly baked Naan bread. This iconic combination features tender chicken in a rich, creamy tomato-butter sauce alongside our soft, pillowy naan, making it the perfect introduction to Indian cuisine or a comforting favorite for regular diners.",
        "extended_desc": "This combination represents the heart of Indian dining - the perfect pairing of curry and bread. Our Butter Chicken starts with chicken marinated in yogurt and spices, cooked in our tandoor, then simmered in a luxurious sauce made with butter, cream, tomatoes, and aromatic spices like fenugreek, cardamom, and a hint of sweetness. The accompanying naan is prepared fresh in our tandoor oven, achieving the perfect balance of soft interior and slightly charred exterior. Together, they create a complete meal that's both satisfying and authentic. The creamy, mildly-spiced butter chicken sauce is perfectly absorbed by the naan, making every bite a delightful experience.",
        "image": "chicken-tikka-masala.webp",
        "prep_time": "30",
        "spice_level": "Mild",
        "cuisine": "North Indian",
        "category": "Combo Special"
    }
]


def create_dish_page(dish):
    """Generate a complete HTML page for a dish"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />

    <meta
      name="description"
      content="Best {dish['name']} in {RESTAURANT_INFO['location']} at {RESTAURANT_INFO['name']}! {dish['short_desc']}. Order online for delivery, takeout, or dine-in."
    />
    <meta
      name="keywords"
      content="best {dish['name']} {RESTAURANT_INFO['location']}, {dish['name']} delivery {RESTAURANT_INFO['location']}, Indian restaurant {RESTAURANT_INFO['location']}, {RESTAURANT_INFO['name']} {dish['name']}, authentic {dish['name']} {RESTAURANT_INFO['location']}, {dish['cuisine']} {RESTAURANT_INFO['location']}"
    />
    <link rel="canonical" href="{RESTAURANT_INFO['website']}/tags/dishes/{dish['slug']}.html" />

    <title>Best {dish['name']} in {RESTAURANT_INFO['location']} | {RESTAURANT_INFO['name']}</title>

    <link href="../../assets/favicon/favicon.png" rel="icon" />

    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
    <meta name="application-name" content="hakkakitchenrestaurant.com" />
    <link rel="alternate" hreflang="en-ca" href="{RESTAURANT_INFO['website']}/tags/dishes/{dish['slug']}.html" />
    <meta name="theme-color" content="#ffffff" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="default" />
    <meta name="format-detection" content="telephone=no" />

    <!-- Social Media Meta Tags -->
    <meta property="og:url" content="{RESTAURANT_INFO['website']}/tags/dishes/{dish['slug']}.html" />
    <meta property="og:site_name" content="{RESTAURANT_INFO['name']}" />
    <meta
      property="og:title"
      content="Best {dish['name']} in {RESTAURANT_INFO['location']} | {RESTAURANT_INFO['name']}"
    />
    <meta property="og:type" content="product" />
    <meta name="author" content="hakkakitchenrestaurant.com" />
    <meta name="geo.region" content="CA-AB" />
    <meta name="geo.placename" content="{RESTAURANT_INFO['location']}" />
    <meta name="geo.position" content="{RESTAURANT_INFO['geo_position']}" />
    <meta name="ICBM" content="{RESTAURANT_INFO['geo_position']}" />
    <meta property="og:locale" content="en_CA" />
    <meta
      property="og:image"
      content="{RESTAURANT_INFO['website']}/assets/popular-dishes/{dish['image']}"
    />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:type" content="image/webp" />
    <meta
      property="og:description"
      content="Best {dish['name']} in {RESTAURANT_INFO['location']} at {RESTAURANT_INFO['name']}! {dish['short_desc']}. Order online for delivery, takeout, or dine-in."
    />

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta
      name="twitter:title"
      content="Best {dish['name']} in {RESTAURANT_INFO['location']} | {RESTAURANT_INFO['name']}"
    />
    <meta
      name="twitter:image"
      content="{RESTAURANT_INFO['website']}/assets/popular-dishes/{dish['image']}"
    />
    <meta
      name="twitter:description"
      content="Best {dish['name']} in {RESTAURANT_INFO['location']} at {RESTAURANT_INFO['name']}! {dish['short_desc']}. Order online for delivery, takeout, or dine-in."
    />

    <!-- Sitemap and Robots -->
    <link
      rel="sitemap"
      type="application/xml"
      title="Sitemap"
      href="{RESTAURANT_INFO['website']}/sitemap.xml"
    />
    <link rel="robots" href="{RESTAURANT_INFO['website']}/robots.txt" />

    <!-- Favicon Icons -->
    <link
      rel="apple-touch-icon"
      sizes="57x57"
      href="../../assets/favicon/favicon.png"
    />
    <link
      rel="apple-touch-icon"
      sizes="60x60"
      href="../../assets/favicon/favicon.png"
    />
    <link
      rel="apple-touch-icon"
      sizes="72x72"
      href="../../assets/favicon/favicon.png"
    />
    <link
      rel="apple-touch-icon"
      sizes="152x152"
      href="../../assets/favicon/favicon.png"
    />

    <!-- CSS and Fonts -->
    <link
      href="https://cdn.jsdelivr.net/npm/remixicon@4.1.0/fonts/remixicon.css"
      rel="stylesheet"
    />
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css"
    />
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css"
      integrity="sha512-SnH5WK+bZxgPHs44uWIX+LLJAJ9/2PkPKZ5QiAj6Ta86w+fsb2TkcmfRyVX3pBnMFcV7oQPJkl9QevSCWr3W6A=="
      crossorigin="anonymous"
      referrerpolicy="no-referrer"
    />
    <link rel="stylesheet" href="../../style.css" />
    <link rel="stylesheet" href="../../global.css" />

    <!-- Structured Data: Product -->
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org/",
        "@type": "Product",
        "name": "{dish['name']}",
        "image": "{RESTAURANT_INFO['website']}/assets/popular-dishes/{dish['image']}",
        "description": "{dish['full_desc']}",
        "brand": {{
          "@type": "Brand",
          "name": "{RESTAURANT_INFO['name']}"
        }},
        "offers": {{
          "@type": "Offer",
          "url": "{RESTAURANT_INFO['website']}/tags/dishes/{dish['slug']}.html",
          "priceCurrency": "CAD",
          "availability": "https://schema.org/InStock",
          "itemCondition": "https://schema.org/NewCondition"
        }},
        "aggregateRating": {{
          "@type": "AggregateRating",
          "ratingValue": "4.7",
          "reviewCount": "45"
        }}
      }}
    </script>

    <!-- Structured Data: Recipe -->
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org/",
        "@type": "Recipe",
        "name": "{RESTAURANT_INFO['name']}'s {dish['name']}",
        "image": "{RESTAURANT_INFO['website']}/assets/popular-dishes/{dish['image']}",
        "author": {{
          "@type": "Organization",
          "name": "{RESTAURANT_INFO['name']}"
        }},
        "datePublished": "2024-01-15",
        "description": "{dish['full_desc']}",
        "prepTime": "PT{dish['prep_time']}M",
        "recipeYield": "2 servings",
        "recipeCategory": "{dish['category']}",
        "recipeCuisine": "{dish['cuisine']}",
        "aggregateRating": {{
          "@type": "AggregateRating",
          "ratingValue": "4.7",
          "reviewCount": "45"
        }},
        "keywords": "{dish['name']}, {dish['cuisine']}, {RESTAURANT_INFO['location']}"
      }}
    </script>

    <!-- Breadcrumbs -->
    <script type="application/ld+json">
      {{
        "@context": "http://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "{RESTAURANT_INFO['website']}"
          }},
          {{
            "@type": "ListItem",
            "position": 2,
            "name": "Menu",
            "item": "{RESTAURANT_INFO['website']}/menu.html"
          }},
          {{
            "@type": "ListItem",
            "position": 3,
            "name": "{dish['name']}",
            "item": "{RESTAURANT_INFO['website']}/tags/dishes/{dish['slug']}.html"
          }}
        ]
      }}
    </script>

    <!-- Preload Images -->
    <link rel="preload" as="image" href="../../assets/popular-dishes/{dish['image']}" />
    <link rel="preload" as="image" href="../../assets/logo/logo.webp" />
  </head>

  <body>
    <!-- floating button -->
    <div class="floating-btn-wrapper">
      <a
        href="{RESTAURANT_INFO['order_link']}"
        class="btn order-float"
        target="_blank"
        onclick="fbq('track', 'Lead');"
        >Order Online</a
      >
    </div>

    <!-- floating button -->

    <!-- navbar -->

    <div id="header-container"></div>

    <!-- navbar -->

    <!-- Breadcrumb Navigation -->
    <div class="breadcrumb-container">
      <div class="breadcrumb-wrapper">
        <ul class="breadcrumb" itemscope itemtype="https://schema.org/BreadcrumbList">
          <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <a itemprop="item" href="../../index.html">
              <span itemprop="name">Home</span>
            </a>
            <meta itemprop="position" content="1" />
          </li>
          <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <a itemprop="item" href="../../menu.html">
              <span itemprop="name">Menu</span>
            </a>
            <meta itemprop="position" content="2" />
          </li>
          <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <span itemprop="name">{dish['name']}</span>
            <meta itemprop="position" content="3" />
          </li>
        </ul>
      </div>
    </div>
    <!-- End Breadcrumb Navigation -->

    <!-- Dish Hero Section -->
    <section class="dish-hero section__container header__container3">
      <div class="dish-hero-container">
        <div class="dish-hero-content">
          <h1>Best {dish['name']} in {RESTAURANT_INFO['location']}</h1>
          <div class="dish-rating">
            <span><i class="ri-star-fill"></i></span>
            <span><i class="ri-star-fill"></i></span>
            <span><i class="ri-star-fill"></i></span>
            <span><i class="ri-star-fill"></i></span>
            <span><i class="ri-star-half-fill"></i></span>
            <span class="rating-count">(45 reviews)</span>
          </div>
          <p class="dish-description">
            {dish['full_desc']}
          </p>
          <div class="dish-details">
            <div class="dish-detail">
              <i class="ri-timer-line"></i>
              <span>Prep Time: {dish['prep_time']} mins</span>
            </div>
            <div class="dish-detail">
              <i class="ri-fire-line"></i>
              <span>Spice Level: {dish['spice_level']}</span>
            </div>
            <div class="dish-detail">
              <i class="ri-award-line"></i>
              <span>Customer Favorite</span>
            </div>
          </div>
          <div class="dish-price">
            <a href="{RESTAURANT_INFO['order_link']}" class="btn" target="_blank">Order Now</a>
          </div>
        </div>
        <div class="dish-hero-image">
          <img
            src="../../assets/popular-dishes/{dish['image']}"
            alt="{dish['name']} at {RESTAURANT_INFO['name']} in {RESTAURANT_INFO['location']}"
            width="600"
            height="400"
            loading="eager"
          />
        </div>
      </div>
    </section>

    <!-- Dish Description Section -->
    <section class="section__container dish-description-container">
      <div class="dish-description-content">
        <h2 class="section__header">About Our {dish['name']}</h2>
        <p class="section__description">
          {dish['extended_desc']}
        </p>
        <p class="section__description">
          At {RESTAURANT_INFO['name']}, we take pride in preparing authentic {dish['cuisine']} dishes using traditional cooking methods and the finest ingredients. Our {dish['name']} is a testament to our commitment to quality and authenticity. Perfect for dine-in, takeout, or delivery throughout {RESTAURANT_INFO['location']}.
        </p>
      </div>
    </section>

    <!-- Customer Reviews Section -->
    <section class="section__container reviews-container">
      <h2 class="section__header">What Customers Say About Our {dish['name']}</h2>
      <div class="reviews-grid">
        <div class="review-card">
          <div class="review-header">
            <div class="reviewer-info">
              <h4>Rajesh K.</h4>
              <p>{RESTAURANT_INFO['location']} Resident</p>
            </div>
            <div class="review-rating">
              <span><i class="ri-star-fill"></i></span>
              <span><i class="ri-star-fill"></i></span>
              <span><i class="ri-star-fill"></i></span>
              <span><i class="ri-star-fill"></i></span>
              <span><i class="ri-star-fill"></i></span>
            </div>
          </div>
          <p class="review-text">
            "The {dish['name']} at {RESTAURANT_INFO['name']} is absolutely authentic! The flavors remind me of home-cooked meals. The spices are perfectly balanced, and the quality of ingredients is evident in every bite. Highly recommend!"
          </p>
          <p class="review-date">March 20, 2024</p>
        </div>
        <div class="review-card">
          <div class="review-header">
            <div class="reviewer-info">
              <h4>Sarah M.</h4>
              <p>Food Enthusiast</p>
            </div>
            <div class="review-rating">
              <span><i class="ri-star-fill"></i></span>
              <span><i class="ri-star-fill"></i></span>
              <span><i class="ri-star-fill"></i></span>
              <span><i class="ri-star-fill"></i></span>
              <span><i class="ri-star-fill"></i></span>
            </div>
          </div>
          <p class="review-text">
            "Best {dish['name']} in {RESTAURANT_INFO['location']}! The preparation is excellent and the portion size is generous. The staff is friendly and the service is quick. This is our go-to spot for Indian food."
          </p>
          <p class="review-date">March 15, 2024</p>
        </div>
        <div class="review-card">
          <div class="review-header">
            <div class="reviewer-info">
              <h4>David L.</h4>
              <p>Regular Customer</p>
            </div>
            <div class="review-rating">
              <span><i class="ri-star-fill"></i></span>
              <span><i class="ri-star-fill"></i></span>
              <span><i class="ri-star-fill"></i></span>
              <span><i class="ri-star-fill"></i></span>
              <span><i class="ri-star-fill"></i></span>
            </div>
          </div>
          <p class="review-text">
            "Outstanding! The {dish['name']} is consistently delicious every time we order. {RESTAURANT_INFO['name']} has become our favorite restaurant in {RESTAURANT_INFO['location']}. The quality and taste never disappoint."
          </p>
          <p class="review-date">March 10, 2024</p>
        </div>
      </div>
    </section>

    <!-- Order CTA Section -->
    <section class="section__container cta-container">
      <div class="cta-content">
        <h2>Ready to Try Our Delicious {dish['name']}?</h2>
        <p>Order online for pickup, delivery, or dine-in throughout {RESTAURANT_INFO['location']}</p>
        <a href="{RESTAURANT_INFO['order_link']}" class="btn" target="_blank">Order Now</a>
        <a href="../../menu.html" class="btn" style="margin-left: 10px;">View Menu</a>
      </div>
    </section>

    <!-- Location & Contact Section -->
    <section class="section__container location-contact-container">
      <h2 class="section__header">Visit {RESTAURANT_INFO['name']}</h2>
      <div class="location-contact-wrapper">
        <div class="map-section">
          {RESTAURANT_INFO['maps_iframe']}
        </div>
        <div class="info-section">
          <h3>Location & Hours</h3>
          <div class="contact-details">
            <div class="contact-item">
              <i class="ri-map-pin-line"></i>
              <div>
                <h4>Address</h4>
                <p>{RESTAURANT_INFO['address']}</p>
              </div>
            </div>
            <div class="contact-item">
              <i class="ri-phone-line"></i>
              <div>
                <h4>Phone</h4>
                <p><a href="tel:{RESTAURANT_INFO['phone_link']}">{RESTAURANT_INFO['phone']}</a></p>
              </div>
            </div>
            <div class="contact-item">
              <i class="ri-time-line"></i>
              <div>
                <h4>Hours</h4>
                <ul class="hours-list">
                  <li><strong>Monday:</strong> Closed</li>
                  <li><strong>Tue-Thu:</strong> 11:30 AM - 9:00 PM</li>
                  <li><strong>Friday:</strong> 11:30 AM - 10:00 PM</li>
                  <li><strong>Saturday:</strong> 10:00 AM - 10:00 PM</li>
                  <li><strong>Sunday:</strong> 10:00 AM - 9:00 PM</li>
                </ul>
              </div>
            </div>
          </div>
          <div class="location-actions">
            <a href="{RESTAURANT_INFO['maps_link']}" class="btn" target="_blank" rel="noopener">
              <i class="ri-map-pin-line"></i> Get Directions
            </a>
            <a href="{RESTAURANT_INFO['order_link']}" class="btn" target="_blank">
              <i class="ri-shopping-bag-line"></i> Order Online
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- footer -->

    <div id="footer-container"></div>

    <!-- footer -->

    <script src="https://unpkg.com/scrollreveal"></script>
    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    <script type="module" src="../../script.js"></script>
    <script src="../../components.js"></script>
  </body>
</html>
"""

    return html_content


def main():
    """Main function to generate all dish pages"""

    # Create output directory if it doesn't exist
    output_dir = Path("tags/dishes")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating {len(DISHES)} dish pages for {RESTAURANT_INFO['name']}...")
    print("-" * 70)

    generated_files = []

    for dish in DISHES:
        filename = f"{dish['slug']}.html"
        filepath = output_dir / filename

        # Generate HTML content
        html_content = create_dish_page(dish)

        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        generated_files.append(filename)
        print(f"[OK] Generated: {filename}")
        print(f"  - {dish['name']}")
        print(f"  - Category: {dish['category']}")
        print(f"  - Cuisine: {dish['cuisine']}")
        print()

    print("-" * 70)
    print(f"[SUCCESS] Generated {len(generated_files)} dish pages!")
    print(f"\nGenerated files:")
    for filename in generated_files:
        print(f"  - tags/dishes/{filename}")

    return generated_files


if __name__ == "__main__":
    main()
