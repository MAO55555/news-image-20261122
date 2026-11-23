#!/usr/bin/env python3
"""
scripts/generate_image.py
Generates the 1024x1024 editorial news poster for Sunday, 22 November 2026.
Bakes /workspace/news-image-20261122/entry.png deterministically.
Also generates /tmp/preview_300.png to verify 300px thumbnail legibility.
"""

import os
import shutil
import subprocess
import sys
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_PNG = os.path.join(PROJECT_DIR, "entry.png")
PREVIEW_300 = "/tmp/preview_300.png"
TMP_HTML = "/tmp/news_entry_render.html"
TMP_PNG = "/tmp/news_entry_chrome.png"
TMP_PROFILE = "/tmp/chrome_news_profile"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  @page {
    size: 1024px 1024px;
    margin: 0;
  }
  html, body {
    width: 1024px;
    height: 1024px;
    overflow: hidden;
    background: #070B12;
    color: #F8FAFC;
    font-family: 'Inter', 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    -webkit-font-smoothing: antialiased;
  }

  .canvas {
    width: 1024px;
    height: 1024px;
    padding: 13px 15px 11px 15px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: radial-gradient(circle at 50% 0%, #141E32 0%, #080D16 60%, #04070D 100%);
    position: relative;
  }

  /* Header Section */
  .header-masthead {
    border-bottom: 2px solid #233145;
    padding-bottom: 7px;
    position: relative;
    z-index: 2;
    flex-shrink: 0;
  }

  .top-meta-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    color: #94A3B8;
    margin-bottom: 2px;
  }
  .pub-name {
    color: #F59E0B;
    font-weight: 800;
    letter-spacing: 1.8px;
  }

  .headline-date-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 1px 0 4px 0;
  }
  .date-title {
    font-family: 'DM Serif Display', 'IBM Plex Serif', 'Playfair Display', serif;
    font-size: 38px;
    font-weight: 900;
    letter-spacing: 1.4px;
    color: #FFFFFF;
    text-transform: uppercase;
    text-shadow: 0 2px 10px rgba(0,0,0,0.6);
    display: flex;
    align-items: center;
    gap: 14px;
  }
  .date-pill {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 800;
    background: #0284C7;
    color: #FFF;
    padding: 3px 9px;
    border-radius: 4px;
    letter-spacing: 1px;
    text-transform: uppercase;
  }

  /* Rapid Alert Strip with ~12px Bold Text */
  .alert-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-top: 3px;
  }
  .alert-item {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 4px;
    padding: 4px 6px;
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 10.8px;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: 0.1px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .pulse-dot {
    width: 7.5px;
    height: 7.5px;
    border-radius: 50%;
    flex-shrink: 0;
  }
  .dot-red { background: #EF4444; box-shadow: 0 0 6px #EF4444; }
  .dot-amber { background: #F59E0B; box-shadow: 0 0 6px #F59E0B; }
  .dot-purple { background: #A855F7; box-shadow: 0 0 6px #A855F7; }

  /* Full-Height 3-Tier Grid Container */
  .news-body-grid {
    flex: 1;
    display: grid;
    grid-template-rows: 1.02fr 1.10fr 1.04fr;
    gap: 12px;
    margin: 8px 0 7px 0;
    min-height: 0;
    position: relative;
    z-index: 2;
  }

  .tier {
    display: grid;
    gap: 12px;
    min-height: 0;
    height: 100%;
  }
  .tier-1 {
    grid-template-columns: 1fr 1fr;
  }
  .tier-2 {
    grid-template-columns: 1fr 1.14fr 1fr;
  }
  .tier-3 {
    grid-template-columns: 1fr 1fr 1fr;
  }

  /* News Card Styles */
  .news-card {
    height: 100%;
    background: rgba(16, 23, 38, 0.92);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 7px;
    padding: 10px 12px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.45);
    position: relative;
    overflow: hidden;
  }
  .news-card::after {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
  }
  .card-emerald::after { background: #10B981; }
  .card-red::after { background: #EF4444; }
  .card-blue::after { background: #38BDF8; }
  .card-amber::after { background: #F59E0B; }
  .card-teal::after { background: #14B8A6; }
  .card-gold::after { background: #EAB308; }
  .card-map::after { background: linear-gradient(90deg, #38BDF8, #818CF8, #C084FC); }

  /* Hero Cards Custom Flow (Bullets directly under headline, vertically centered with diagram) */
  .card-hero {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }
  .card-hero .card-headline.large {
    margin-bottom: 0;
  }
  .card-hero-body {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 10px;
  }
  .hero-bullets {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .hero-bullets .bullet-item {
    font-size: 14.8px;
    line-height: 1.34;
  }
  .diagram-box.hero-diagram {
    width: 156px;
    flex-shrink: 0;
    background: rgba(9, 14, 24, 0.94);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 5px;
    padding: 5px 3px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
  }
  .hero-diagram .diagram-label {
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    color: #94A3B8;
    margin-top: 4px;
    letter-spacing: 0.5px;
  }
  .hero-diagram .diagram-val {
    font-size: 13px;
    font-weight: 900;
    margin-top: 1px;
  }

  .card-top-content {
    display: flex;
    flex-direction: column;
  }

  .card-badge-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 5px;
  }
  .badge {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    padding: 2.5px 7px;
    border-radius: 3px;
    display: inline-flex;
    align-items: center;
    gap: 5px;
  }
  .badge-emerald { background: rgba(16, 185, 129, 0.2); color: #6EE7B7; border: 1px solid rgba(16, 185, 129, 0.4); }
  .badge-red { background: rgba(239, 68, 68, 0.2); color: #FCA5A5; border: 1px solid rgba(239, 68, 68, 0.4); }
  .badge-blue { background: rgba(56, 189, 248, 0.2); color: #7DD3FC; border: 1px solid rgba(56, 189, 248, 0.4); }
  .badge-amber { background: rgba(245, 158, 11, 0.2); color: #FCD34D; border: 1px solid rgba(245, 158, 11, 0.4); }
  .badge-teal { background: rgba(20, 184, 166, 0.2); color: #5EEAD4; border: 1px solid rgba(20, 184, 166, 0.4); }
  .badge-gold { background: rgba(234, 179, 8, 0.2); color: #FDE047; border: 1px solid rgba(234, 179, 8, 0.4); }

  .stat-pill {
    font-size: 10.5px;
    font-weight: 700;
    color: #94A3B8;
    background: rgba(255, 255, 255, 0.06);
    padding: 2.5px 7px;
    border-radius: 3px;
    letter-spacing: 0.5px;
  }

  /* Headlines */
  .card-headline {
    font-size: 19px;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.22;
    margin-bottom: 7px;
    letter-spacing: -0.3px;
  }
  .card-headline.large {
    font-size: 22px;
    line-height: 1.22;
    letter-spacing: -0.4px;
  }

  .card-bullets {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .bullet-item {
    font-size: 14px;
    line-height: 1.35;
    color: #CBD5E1;
    position: relative;
    padding-left: 12px;
  }
  .bullet-item::before {
    content: "■";
    position: absolute;
    left: 0;
    top: 1px;
    font-size: 8px;
    color: #64748B;
  }
  .bullet-item strong {
    color: #F8FAFC;
    font-weight: 750;
  }

  /* Pictogram Strips for Tier 2/3 Cards (~64px tall, non-overlapping) */
  .card-pictogram-strip {
    display: flex;
    justify-content: flex-end;
    align-items: flex-end;
    padding-top: 4px;
    margin-top: auto;
  }

  /* World Map Card */
  .map-card {
    background: rgba(11, 17, 29, 0.96);
    padding: 8px 10px 6px 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .map-container {
    width: 100%;
    flex: 1;
    min-height: 216px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  /* Editorial Dateline Footer (strictly single-line) */
  .footer-bar {
    border-top: 1px solid #233145;
    padding-top: 6px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 10px;
    font-weight: 700;
    color: #94A3B8;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    white-space: nowrap;
    position: relative;
    z-index: 2;
    flex-shrink: 0;
  }
  .footer-bar span.accent {
    color: #F8FAFC;
    font-weight: 800;
  }
</style>
</head>
<body>
<div class="canvas">

  <!-- HEADER MASTHEAD -->
  <div class="header-masthead">
    <div class="top-meta-row">
      <div class="pub-name">WORLD NEWS SUMMARY</div>
      <div>22 NOV 2026 · FULL DAY REVIEW</div>
    </div>

    <div class="headline-date-row">
      <div class="date-title">
        SUNDAY, 22 NOVEMBER 2026
        <span class="date-pill">WORLD EDITION</span>
      </div>
    </div>

    <!-- Alert Strip with 4 Key Flashpoints (Clean fit, zero clipping) -->
    <div class="alert-strip">
      <div class="alert-item">
        <div class="pulse-dot dot-red"></div>
        <span>COP31 COLLAPSES: NO DEAL</span>
      </div>
      <div class="alert-item">
        <div class="pulse-dot dot-red"></div>
        <span>HORMUZ: IRAN CLAIMS MINES</span>
      </div>
      <div class="alert-item">
        <div class="pulse-dot dot-amber"></div>
        <span>RUSSIAN DRONE KILLS 6 NEAR KYIV</span>
      </div>
      <div class="alert-item">
        <div class="pulse-dot dot-purple"></div>
        <span>VERSTAPPEN WINS VEGAS GP</span>
      </div>
    </div>
  </div>

  <!-- FULL-HEIGHT 3-TIER GRID -->
  <div class="news-body-grid">

    <!-- TIER 1: LEAD HERO CARDS (COP31 & Middle East) -->
    <div class="tier tier-1">
      
      <!-- CLIMATE / COP31 COLLAPSE (Lead Hero Left) -->
      <div class="news-card card-emerald card-hero">
        <div class="card-badge-row">
          <div class="badge badge-emerald">
            <svg width="10" height="10" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
            CLIMATE / UN
          </div>
          <div class="stat-pill">ANTALYA, TÜRKİYE</div>
        </div>
        <div class="card-headline large">
          COP31 Collapses Without a Deal After Record Overtime
        </div>
        <div class="card-hero-body">
          <div class="card-bullets hero-bullets">
            <div class="bullet-item">EU, Panama and Marshall Islands rejected final text for omitting fossil fuels.</div>
            <div class="bullet-item">COP31 president Kurum: "There is nothing to do." Guterres: "deeply disappointing."</div>
          </div>
          <!-- Diagram: COP31 Status (~156px wide, zero overlap) -->
          <div class="diagram-box hero-diagram">
            <svg width="148" height="96" viewBox="0 0 148 96">
              <rect width="148" height="96" rx="4" fill="#0A1619"/>
              <text x="74" y="14" fill="#6EE7B7" font-size="11" font-weight="800" text-anchor="middle">COP31 TEXT STATUS</text>
              <rect x="6" y="22" width="136" height="20" rx="3" fill="#334155"/>
              <text x="74" y="36.5" fill="#FFFFFF" font-size="11" font-weight="800" text-anchor="middle">FINAL TEXT REJECTED</text>
              <rect x="6" y="47" width="136" height="22" rx="3" fill="#DC2626"/>
              <text x="74" y="63" fill="#FFFFFF" font-size="13" font-weight="900" text-anchor="middle">COLLAPSED</text>
              <rect x="4" y="73" width="78" height="19" rx="3" fill="#1E293B"/>
              <text x="43" y="86.5" fill="#E2E8F0" font-size="9.5" font-weight="700" text-anchor="middle">~200 NATIONS</text>
              <rect x="86" y="73" width="58" height="19" rx="3" fill="#991B1B"/>
              <text x="115" y="86.5" fill="#FCA5A5" font-size="9.5" font-weight="900" text-anchor="middle">NO DEAL</text>
            </svg>
            <div class="diagram-label">FOSSIL FUELS & FINANCE</div>
            <div class="diagram-val" style="color:#EF4444;">COLLAPSED</div>
          </div>
        </div>
      </div>

      <!-- MIDDLE EAST & GULF (Hero Right) -->
      <div class="news-card card-red card-hero">
        <div class="card-badge-row">
          <div class="badge badge-red">
            <svg width="10" height="10" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2L1 21h22L12 2zm0 3.8L20 19H4l8-13.2zM11 10h2v4h-2zm0 6h2v2h-2z"/></svg>
            MIDDLE EAST / GULF
          </div>
          <div class="stat-pill">HORMUZ · IRAN</div>
        </div>
        <div class="card-headline large">
          Iran Says Two Supertankers Hit Mines Near Hormuz
        </div>
        <div class="card-hero-body">
          <div class="card-bullets hero-bullets">
            <div class="bullet-item">IRGC navy: tankers exploded east of Strait of Hormuz (Iranian claim; unconfirmed). UKMTO reported incident in Gulf of Oman.</div>
            <div class="bullet-item">Iran began rolling power cuts. Houthis CLAIMED strike on Saudi Rabigh refinery (Saudi Arabia did not confirm).</div>
          </div>
          <!-- Diagram: Hormuz Mines (~156px wide, zero overlap) -->
          <div class="diagram-box hero-diagram">
            <svg width="148" height="96" viewBox="0 0 148 96">
              <rect width="148" height="96" rx="4" fill="#120A0A"/>
              <text x="74" y="14" fill="#F87171" font-size="11.5" font-weight="800" text-anchor="middle">STRAIT OF HORMUZ</text>
              <path d="M 8 22 Q 56 32 74 18 Q 100 12 140 16 L 140 78 Q 100 66 74 74 Q 40 84 8 72 Z" fill="#1E293B" opacity="0.45"/>
              <path d="M 12 48 Q 74 52 136 46" fill="none" stroke="#64748B" stroke-width="1.5" stroke-dasharray="4,3"/>
              <!-- Mine 1 -->
              <circle cx="38" cy="46" r="8" fill="#EF4444" fill-opacity="0.35"/>
              <circle cx="38" cy="46" r="3.5" fill="#EF4444"/>
              <line x1="38" y1="38" x2="38" y2="54" stroke="#F59E0B" stroke-width="1.2"/>
              <line x1="30" y1="46" x2="46" y2="46" stroke="#F59E0B" stroke-width="1.2"/>
              <!-- Mine 2 -->
              <circle cx="110" cy="44" r="8" fill="#EF4444" fill-opacity="0.35"/>
              <circle cx="110" cy="44" r="3.5" fill="#EF4444"/>
              <line x1="110" y1="36" x2="110" y2="52" stroke="#F59E0B" stroke-width="1.2"/>
              <line x1="102" y1="44" x2="118" y2="44" stroke="#F59E0B" stroke-width="1.2"/>
              <text x="38" y="63" fill="#FCD34D" font-size="9.5" font-weight="800" text-anchor="middle">TANKER 1</text>
              <text x="110" y="61" fill="#FCD34D" font-size="9.5" font-weight="800" text-anchor="middle">TANKER 2</text>
              <text x="74" y="85" fill="#CBD5E1" font-size="10" font-weight="700" text-anchor="middle">UNCONFIRMED CLAIM</text>
            </svg>
            <div class="diagram-label">HORMUZ STRAIT</div>
            <div class="diagram-val" style="color:#EF4444;">MINES (CLAIM)</div>
          </div>
        </div>
      </div>

    </div>

    <!-- TIER 2: EUROPE / UKRAINE, WORLD MAP, AFRICA -->
    <div class="tier tier-2">
      
      <!-- EUROPE / UKRAINE -->
      <div class="news-card card-blue">
        <div class="card-top-content">
          <div class="card-badge-row">
            <div class="badge badge-blue">EUROPE / UKRAINE</div>
            <div class="stat-pill">KYIV REGION</div>
          </div>
          <div class="card-headline">
            Russian Drone Collapses Apartment Block Near Kyiv
          </div>
          <div class="card-bullets">
            <div class="bullet-item">Shahed drone destroyed section of 5-storey building in Dymer overnight; at least 6 killed, boy pulled alive.</div>
            <div class="bullet-item">Two more killed in Russian strike on Vyshneve supermarket. Kyiv region declared 23 Nov day of mourning.</div>
          </div>
        </div>
        <!-- Pictogram: Damaged apartment block with drone (~64px tall) -->
        <div class="card-pictogram-strip">
          <svg width="84" height="64" viewBox="0 0 84 64">
            <line x1="4" y1="58" x2="80" y2="58" stroke="#38BDF8" stroke-width="2" stroke-linecap="round"/>
            <path d="M 8 58 L 8 18 L 30 18 L 36 28 L 46 22 L 52 58 Z" fill="#1E293B" stroke="#38BDF8" stroke-width="2"/>
            <rect x="14" y="25" width="6" height="6" rx="1" fill="#38BDF8"/>
            <rect x="25" y="30" width="6" height="6" rx="1" fill="#38BDF8"/>
            <rect x="14" y="38" width="6" height="6" rx="1" fill="#38BDF8"/>
            <rect x="25" y="44" width="6" height="6" rx="1" fill="#38BDF8"/>
            <circle cx="43" cy="26" r="2" fill="#F87171"/>
            <circle cx="48" cy="20" r="2.5" fill="#F87171"/>
            <ellipse cx="66" cy="16" rx="5" ry="2.5" fill="#F87171"/>
            <line x1="56" y1="12" x2="76" y2="20" stroke="#F87171" stroke-width="1.8"/>
            <line x1="56" y1="20" x2="76" y2="12" stroke="#F87171" stroke-width="1.8"/>
            <line x1="53" y1="12" x2="59" y2="12" stroke="#38BDF8" stroke-width="1.5"/>
            <line x1="73" y1="20" x2="79" y2="20" stroke="#38BDF8" stroke-width="1.5"/>
            <line x1="53" y1="20" x2="59" y2="20" stroke="#38BDF8" stroke-width="1.5"/>
            <line x1="73" y1="12" x2="79" y2="12" stroke="#38BDF8" stroke-width="1.5"/>
          </svg>
        </div>
      </div>

      <!-- CENTRAL WORLD INCIDENT MAP (Scaled land masses filling card, 9 accurate pins) -->
      <div class="news-card card-map map-card">
        <div class="card-badge-row">
          <div class="badge" style="background:rgba(99,102,241,0.22); color:#A5B4FC; border:1px solid rgba(99,102,241,0.45);">
            22 NOV GLOBAL MAP
          </div>
          <div class="stat-pill" style="color:#38BDF8;">9 HOTSPOTS</div>
        </div>
        
        <!-- Scaled SVG World Map Filling Card Height & Width -->
        <div class="map-container">
          <svg width="340" height="216" viewBox="0 0 340 216">
            <!-- Background & Coordinate Grid -->
            <rect width="340" height="216" rx="4" fill="#0A111E"/>
            <line x1="0" y1="72" x2="340" y2="72" stroke="#1E293B" stroke-width="0.8"/>
            <line x1="0" y1="144" x2="340" y2="144" stroke="#1E293B" stroke-width="0.8"/>
            <line x1="85" y1="0" x2="85" y2="216" stroke="#1E293B" stroke-width="0.8"/>
            <line x1="170" y1="0" x2="170" y2="216" stroke="#1E293B" stroke-width="0.8"/>
            <line x1="255" y1="0" x2="255" y2="216" stroke="#1E293B" stroke-width="0.8"/>

            <!-- High-Contrast World Continents Filling the Card -->
            <!-- North America & Arctic -->
            <path d="M 18 20 L 72 14 L 110 32 L 105 84 L 88 108 L 74 92 L 44 76 L 14 56 Z" fill="#1C283C" stroke="#334A6E" stroke-width="1.2"/>
            <path d="M 96 90 L 104 94 L 102 112 L 96 112 L 94 98 Z" fill="#1C283C" stroke="#334A6E" stroke-width="1.2"/>
            <!-- South America -->
            <path d="M 85 118 L 122 122 L 116 172 L 98 206 L 82 168 Z" fill="#1C283C" stroke="#334A6E" stroke-width="1.2"/>
            <!-- Europe & Scandinavia -->
            <path d="M 160 22 L 206 18 L 204 74 L 172 78 L 162 60 Z" fill="#1C283C" stroke="#334A6E" stroke-width="1.2"/>
            <!-- Africa -->
            <path d="M 164 88 L 216 88 L 222 144 L 194 196 L 172 152 L 164 114 Z" fill="#1C283C" stroke="#334A6E" stroke-width="1.2"/>
            <!-- Asia & Siberia -->
            <path d="M 208 16 L 324 16 L 334 76 L 286 104 L 242 98 L 218 68 Z" fill="#1C283C" stroke="#334A6E" stroke-width="1.2"/>
            <!-- Japan -->
            <path d="M 318 46 L 330 46 L 324 74 L 316 74 Z" fill="#1C283C" stroke="#334A6E" stroke-width="1.2"/>
            <!-- Southeast Asia -->
            <path d="M 268 100 L 290 108 L 302 136 L 278 138 Z" fill="#1C283C" stroke="#334A6E" stroke-width="1.2"/>
            <!-- Australia -->
            <path d="M 296 154 L 338 154 L 332 198 L 302 194 Z" fill="#1C283C" stroke="#334A6E" stroke-width="1.2"/>

            <!-- 9 Geographically Accurate Pins with Bold Labels (>= 10px, Zero Collisions) -->
            <!-- 1. Las Vegas (South-Western US) -->
            <circle cx="54" cy="70" r="3.6" fill="#EAB308"/>
            <line x1="54" y1="70" x2="38" y2="58" stroke="#EAB308" stroke-width="1"/>
            <text x="10" y="56" fill="#FDE047" font-size="10.5" font-weight="900" text-anchor="start">LAS VEGAS</text>

            <!-- 2. Florida (South-East US Peninsula) -->
            <circle cx="100" cy="102" r="3.6" fill="#F59E0B"/>
            <line x1="100" y1="102" x2="88" y2="116" stroke="#F59E0B" stroke-width="1"/>
            <text x="68" y="126" fill="#FCD34D" font-size="10.5" font-weight="900" text-anchor="start">FLORIDA</text>

            <!-- 3. Kyiv (North of Black Sea) -->
            <circle cx="202" cy="58" r="3.6" fill="#38BDF8"/>
            <line x1="202" y1="58" x2="202" y2="42" stroke="#38BDF8" stroke-width="1"/>
            <text x="202" y="38" fill="#7DD3FC" font-size="10.5" font-weight="900" text-anchor="middle">KYIV</text>

            <!-- 4. Antalya (Southern Coast of Türkiye) -->
            <circle cx="200" cy="82" r="3.6" fill="#10B981"/>
            <line x1="200" y1="82" x2="180" y2="82" stroke="#10B981" stroke-width="1"/>
            <text x="174" y="85" fill="#6EE7B7" font-size="10.5" font-weight="900" text-anchor="end">ANTALYA</text>

            <!-- 5. Hormuz (Mouth of Persian Gulf) -->
            <circle cx="232" cy="96" r="3.8" fill="#EF4444"/>
            <line x1="232" y1="96" x2="248" y2="96" stroke="#EF4444" stroke-width="1"/>
            <text x="252" y="99" fill="#FCA5A5" font-size="10.5" font-weight="900" text-anchor="start">HORMUZ</text>

            <!-- 6. Khartoum (North-East Africa on the Nile) -->
            <circle cx="208" cy="120" r="3.6" fill="#F59E0B"/>
            <line x1="208" y1="120" x2="218" y2="148" stroke="#F59E0B" stroke-width="1"/>
            <text x="220" y="158" fill="#FCD34D" font-size="10.5" font-weight="900" text-anchor="start">KHARTOUM</text>

            <!-- 7. Bayelsa (Southern Nigeria, Gulf of Guinea Coast) -->
            <circle cx="180" cy="138" r="3.6" fill="#F59E0B"/>
            <line x1="180" y1="138" x2="160" y2="146" stroke="#F59E0B" stroke-width="1"/>
            <text x="154" y="150" fill="#FCD34D" font-size="10.5" font-weight="900" text-anchor="end">BAYELSA</text>

            <!-- 8. Myanmar (South-East Asia) -->
            <circle cx="272" cy="106" r="3.6" fill="#14B8A6"/>
            <line x1="272" y1="106" x2="282" y2="117" stroke="#14B8A6" stroke-width="1"/>
            <text x="284" y="128" fill="#5EEAD4" font-size="10.5" font-weight="900" text-anchor="middle">MYANMAR</text>

            <!-- 9. Fukushima (North-East Honshu, Japan) -->
            <circle cx="324" cy="60" r="3.6" fill="#FFFFFF"/>
            <line x1="324" y1="60" x2="334" y2="54" stroke="#FFFFFF" stroke-width="1"/>
            <text x="334" y="52" fill="#FFFFFF" font-size="10.5" font-weight="900" text-anchor="end">FUKUSHIMA</text>
          </svg>
        </div>

        <div style="font-size:8.5px; text-align:center; color:#94A3B8; font-weight:700; margin-top:2px;">
          SUNDAY, 22 NOVEMBER 2026 — GLOBAL HOTSPOTS
        </div>
      </div>

      <!-- AFRICA -->
      <div class="news-card card-amber">
        <div class="card-top-content">
          <div class="card-badge-row">
            <div class="badge badge-amber">AFRICA</div>
            <div class="stat-pill">SUDAN · NIGERIA</div>
          </div>
          <div class="card-headline">
            Sudan Drone Strikes Hit Capital; Nigeria Boat Toll 29
          </div>
          <div class="card-bullets">
            <div class="bullet-item">RSF-blamed drones hit Khartoum and Omdurman early Sunday; 4 killed, UN building damaged with staff inside.</div>
            <div class="bullet-item">Nigeria: death toll from Bayelsa boat accident rose to 29; more than 50 survivors.</div>
          </div>
        </div>
        <!-- Pictogram: Drone over buildings + small boat (~64px tall) -->
        <div class="card-pictogram-strip">
          <svg width="84" height="64" viewBox="0 0 84 64">
            <rect x="4" y="30" width="14" height="28" fill="#1E293B" stroke="#F59E0B" stroke-width="2"/>
            <rect x="21" y="22" width="16" height="36" fill="#1E293B" stroke="#F59E0B" stroke-width="2"/>
            <rect x="8" y="35" width="4" height="4" fill="#F59E0B"/>
            <rect x="8" y="46" width="4" height="4" fill="#F59E0B"/>
            <rect x="26" y="29" width="4" height="4" fill="#F59E0B"/>
            <rect x="26" y="40" width="4" height="4" fill="#F59E0B"/>
            <ellipse cx="20" cy="10" rx="4.5" ry="2.2" fill="#F59E0B"/>
            <line x1="11" y1="7" x2="29" y2="13" stroke="#F59E0B" stroke-width="1.5"/>
            <line x1="11" y1="13" x2="29" y2="7" stroke="#F59E0B" stroke-width="1.5"/>
            <path d="M 44 54 Q 52 50 60 54 Q 68 58 76 54 Q 80 52 82 54" fill="none" stroke="#38BDF8" stroke-width="2" stroke-linecap="round"/>
            <path d="M 48 60 Q 56 56 64 60 Q 72 64 80 60" fill="none" stroke="#38BDF8" stroke-width="2" stroke-linecap="round"/>
            <path d="M 48 46 L 53 52 L 71 52 L 76 46 Z" fill="#F59E0B"/>
            <line x1="62" y1="46" x2="62" y2="33" stroke="#F59E0B" stroke-width="2"/>
            <polygon points="62,33 62,42 72,42" fill="#38BDF8"/>
          </svg>
        </div>
      </div>

    </div>

    <!-- TIER 3: ASIA-PACIFIC, AMERICAS, GLOBAL SPORT -->
    <div class="tier tier-3">
      
      <!-- ASIA-PACIFIC -->
      <div class="news-card card-teal">
        <div class="card-top-content">
          <div class="card-badge-row">
            <div class="badge badge-teal">ASIA-PACIFIC</div>
            <div class="stat-pill">MYANMAR · JAPAN</div>
          </div>
          <div class="card-headline">
            France Urges UNSC Action on Myanmar After ICJ Ruling
          </div>
          <div class="card-bullets">
            <div class="bullet-item">Myanmar junta rejected ICJ genocide ruling on Rohingya; France called for UN Security Council action.</div>
            <div class="bullet-item">Japan: road access restored to Fukushima's Kitashiobara village after heavy snow isolated ~1,000 residents.</div>
          </div>
        </div>
        <!-- Pictogram: Scales of justice + snowflake (~64px tall) -->
        <div class="card-pictogram-strip">
          <svg width="84" height="64" viewBox="0 0 84 64">
            <line x1="6" y1="56" x2="32" y2="56" stroke="#14B8A6" stroke-width="2.5" stroke-linecap="round"/>
            <line x1="19" y1="56" x2="19" y2="14" stroke="#14B8A6" stroke-width="2.5"/>
            <line x1="4" y1="18" x2="34" y2="18" stroke="#14B8A6" stroke-width="2.2" stroke-linecap="round"/>
            <circle cx="19" cy="14" r="2.5" fill="#14B8A6"/>
            <line x1="6" y1="18" x2="3" y2="32" stroke="#14B8A6" stroke-width="1.2"/>
            <line x1="6" y1="18" x2="11" y2="32" stroke="#14B8A6" stroke-width="1.2"/>
            <path d="M 2 32 Q 7 38 12 32 Z" fill="#14B8A6"/>
            <line x1="32" y1="18" x2="27" y2="32" stroke="#14B8A6" stroke-width="1.2"/>
            <line x1="32" y1="18" x2="35" y2="32" stroke="#14B8A6" stroke-width="1.2"/>
            <path d="M 26 32 Q 31 38 36 32 Z" fill="#14B8A6"/>
            <g transform="translate(60, 32)">
              <line x1="0" y1="-22" x2="0" y2="22" stroke="#F8FAFC" stroke-width="2.2" stroke-linecap="round"/>
              <line x1="-19" y1="-11" x2="19" y2="11" stroke="#F8FAFC" stroke-width="2.2" stroke-linecap="round"/>
              <line x1="-19" y1="11" x2="19" y2="-11" stroke="#F8FAFC" stroke-width="2.2" stroke-linecap="round"/>
              <path d="M -5 -15 L 0 -20 L 5 -15" fill="none" stroke="#F8FAFC" stroke-width="1.8" stroke-linecap="round"/>
              <path d="M -5 15 L 0 20 L 5 15" fill="none" stroke="#F8FAFC" stroke-width="1.8" stroke-linecap="round"/>
              <circle cx="0" cy="0" r="3.5" fill="#14B8A6"/>
            </g>
          </svg>
        </div>
      </div>

      <!-- AMERICAS -->
      <div class="news-card card-amber">
        <div class="card-top-content">
          <div class="card-badge-row">
            <div class="badge badge-amber">AMERICAS</div>
            <div class="stat-pill">US HOUSE · FLORIDA</div>
          </div>
          <div class="card-headline">
            Democrats Win Largest US House Majority This Century
          </div>
          <div class="card-bullets">
            <div class="bullet-item">Democrats secured 258+ seats after Chuck Hubbard projected to beat Rep. Virginia Foxx in NC-5 (22 Nov).</div>
            <div class="bullet-item">Florida: St. Johns River at record/major flood stage from Cocoa to DeLand; flooding expected to last weeks.</div>
          </div>
        </div>
        <!-- Pictogram: Capitol dome + water waves (~64px tall) -->
        <div class="card-pictogram-strip">
          <svg width="84" height="64" viewBox="0 0 84 64">
            <rect x="22" y="30" width="40" height="8" fill="#1E293B" stroke="#F59E0B" stroke-width="1.8"/>
            <line x1="28" y1="30" x2="28" y2="38" stroke="#F59E0B" stroke-width="1.5"/>
            <line x1="35" y1="30" x2="35" y2="38" stroke="#F59E0B" stroke-width="1.5"/>
            <line x1="42" y1="30" x2="42" y2="38" stroke="#F59E0B" stroke-width="1.5"/>
            <line x1="49" y1="30" x2="49" y2="38" stroke="#F59E0B" stroke-width="1.5"/>
            <line x1="56" y1="30" x2="56" y2="38" stroke="#F59E0B" stroke-width="1.5"/>
            <rect x="27" y="21" width="30" height="9" fill="#1E293B" stroke="#F59E0B" stroke-width="1.8"/>
            <path d="M 27 21 Q 42 3 57 21 Z" fill="#F59E0B"/>
            <rect x="39.5" y="2" width="5" height="5" fill="#F59E0B"/>
            <line x1="42" y1="2" x2="42" y2="-1" stroke="#F59E0B" stroke-width="1.8"/>
            <path d="M 6 48 Q 21 42 36 48 Q 51 54 66 48 Q 74 44 80 48" fill="none" stroke="#38BDF8" stroke-width="2.5" stroke-linecap="round"/>
            <path d="M 2 57 Q 17 51 32 57 Q 47 63 62 57 Q 72 53 82 57" fill="none" stroke="#38BDF8" stroke-width="2.5" stroke-linecap="round"/>
          </svg>
        </div>
      </div>

      <!-- GLOBAL SPORT -->
      <div class="news-card card-gold">
        <div class="card-top-content">
          <div class="card-badge-row">
            <div class="badge badge-gold">GLOBAL SPORT</div>
            <div class="stat-pill">F1 · ATP FINALS</div>
          </div>
          <div class="card-headline">
            Verstappen Wins Vegas GP; Alcaraz Takes ATP Finals
          </div>
          <div class="card-bullets">
            <div class="bullet-item">F1: Verstappen won Las Vegas GP from pole; Norris 2nd, Piastri 3rd. 35 lead changes.</div>
            <div class="bullet-item">Tennis: Alcaraz beat world No.1 Zverev <span style="white-space: nowrap;">6-2, 7-6(7)</span> in Turin — his first ATP Finals title.</div>
          </div>
        </div>
        <!-- Pictogram: Chequered flag + tennis racket/ball (~64px tall) -->
        <div class="card-pictogram-strip">
          <svg width="84" height="64" viewBox="0 0 84 64">
            <line x1="8" y1="6" x2="8" y2="58" stroke="#FDE047" stroke-width="2.5" stroke-linecap="round"/>
            <path d="M 9 9 Q 20 6 30 11 Q 36 15 40 12 L 40 33 Q 32 35 27 31 Q 18 27 9 30 Z" fill="#FDE047"/>
            <rect x="9" y="9" width="7" height="6" fill="#0F172A"/>
            <rect x="24" y="10" width="8" height="6" fill="#0F172A"/>
            <rect x="16" y="16" width="8" height="6" fill="#0F172A"/>
            <rect x="32" y="16" width="8" height="6" fill="#0F172A"/>
            <rect x="9" y="23" width="7" height="6" fill="#0F172A"/>
            <rect x="25" y="24" width="8" height="6" fill="#0F172A"/>
            <g transform="translate(60, 32) rotate(-25)">
              <ellipse cx="0" cy="-18" rx="13" ry="17" fill="none" stroke="#FFFFFF" stroke-width="2.2"/>
              <line x1="-8" y1="-18" x2="8" y2="-18" stroke="#FDE047" stroke-width="1.2"/>
              <line x1="0" y1="-30" x2="0" y2="-6" stroke="#FDE047" stroke-width="1.2"/>
              <path d="M -5 -2 L -2.5 8 L 2.5 8 L 5 -2" fill="#FFFFFF"/>
              <rect x="-3" y="8" width="6" height="18" rx="1.5" fill="#FDE047"/>
            </g>
            <circle cx="75" cy="14" r="6" fill="#FDE047"/>
            <path d="M 71 9 Q 76 14 71 19" fill="none" stroke="#0F172A" stroke-width="1.2"/>
          </svg>
        </div>
      </div>

    </div>

  </div>

  <!-- EDITORIAL DATELINE FOOTER (Strictly single line) -->
  <div class="footer-bar">
    <div>WORLD NEWS SUMMARY · <span class="accent">SUNDAY, 22 NOVEMBER 2026</span></div>
    <div><span class="accent">7 REGIONS</span> · SOURCES: UN, REUTERS, AP, AFP, BBC</div>
  </div>

</div>
</body>
</html>
"""

def generate_image():
    print("[*] Generating HTML...")
    with open(TMP_HTML, "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE)

    # Ensure profile directory exists and remove any dangling Singleton locks
    os.makedirs(TMP_PROFILE, exist_ok=True)
    for fname in os.listdir(TMP_PROFILE):
        if fname.startswith("Singleton"):
            try:
                fpath = os.path.join(TMP_PROFILE, fname)
                os.unlink(fpath)
            except OSError:
                pass

    if os.path.exists(TMP_PNG):
        os.remove(TMP_PNG)

    print("[*] Launching headless Chrome screenshot with timeout...")
    chrome_cmd = (
        f"rm -f {TMP_PROFILE}/Singleton* && "
        f"timeout 60s /opt/google/chrome/chrome "
        f"--headless=new "
        f"--disable-gpu "
        f"--no-sandbox "
        f"--disable-background-networking "
        f"--disable-default-apps "
        f"--disable-extensions "
        f"--disable-sync "
        f"--disable-translate "
        f"--metrics-recording-only "
        f"--no-first-run "
        f"--safebrowsing-disable-auto-update "
        f"--disable-component-update "
        f'--host-rules="MAP * ~NOTFOUND" '
        f"--user-data-dir={TMP_PROFILE} "
        f"--window-size=1024,1024 "
        f"--screenshot={TMP_PNG} "
        f"file://{TMP_HTML} > /tmp/chrome_gen.log 2>&1"
    )

    rc = os.system(chrome_cmd)
    if not os.path.exists(TMP_PNG):
        print(f"[*] First attempt returned {rc}, retrying once with clean lock...")
        os.system(f"rm -f {TMP_PROFILE}/Singleton*")
        rc = os.system(chrome_cmd)

    if not os.path.exists(TMP_PNG):
        print(f"[!] Chrome command failed with return code {rc}, log output:")
        if os.path.exists("/tmp/chrome_gen.log"):
            with open("/tmp/chrome_gen.log") as lf:
                print(lf.read()[-500:])
        sys.exit(1)

    print("[*] Processing image with Pillow...")
    img = Image.open(TMP_PNG)
    if img.size != (1024, 1024):
        print(f"[!] Resizing from {img.size} to (1024, 1024)...")
        img = img.resize((1024, 1024), Image.Resampling.LANCZOS)
    img = img.convert("RGB")

    # Save deterministic PNG directly to workspace deliverable
    img.save(OUTPUT_PNG, format="PNG", optimize=True)

    # Also generate a 300x300 preview to verify legibility at scale
    preview_300 = img.resize((300, 300), Image.Resampling.LANCZOS)
    preview_300.save(PREVIEW_300, format="PNG", optimize=True)

    # Cleanup temp scratch files outside workspace
    if os.path.exists(TMP_HTML):
        os.remove(TMP_HTML)
    if os.path.exists(TMP_PNG):
        os.remove(TMP_PNG)
    # Note: Keep TMP_PROFILE cached to avoid 20s re-initialization on subsequent runs

    file_size = os.path.getsize(OUTPUT_PNG)
    preview_size = os.path.getsize(PREVIEW_300)
    print(f"[✓] Successfully generated {OUTPUT_PNG}")
    print(f"    Dimensions: {img.size[0]}x{img.size[1]} px")
    print(f"    File size:  {file_size:,} bytes ({file_size / 1024:.1f} KiB)")
    print(f"[✓] Generated thumbnail preview: {PREVIEW_300} ({preview_size:,} bytes)")

    if file_size > 1024 * 1024:
        raise ValueError(f"Image exceeds 1 MiB limit! Size: {file_size} bytes")

if __name__ == "__main__":
    generate_image()
