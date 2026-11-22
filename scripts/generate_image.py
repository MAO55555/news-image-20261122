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

  /* Tactical Grid Pattern */
  .canvas::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: 
      linear-gradient(rgba(255, 255, 255, 0.025) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255, 255, 255, 0.025) 1px, transparent 1px);
    background-size: 32px 32px;
    pointer-events: none;
  }

  /* Header Section */
  .header-masthead {
    border-bottom: 2px solid #233145;
    padding-bottom: 7px;
    position: relative;
    z-index: 2;
  }

  .top-meta-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    color: #94A3B8;
    margin-bottom: 3px;
  }
  .pub-name {
    color: #F59E0B;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .pub-badge {
    background: rgba(245, 158, 11, 0.16);
    border: 1px solid #F59E0B;
    color: #FBBF24;
    padding: 1px 6px;
    border-radius: 3px;
    font-size: 8.5px;
    font-weight: 800;
  }

  .headline-date-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 2px 0 4px 0;
  }
  .date-title {
    font-family: 'DM Serif Display', 'IBM Plex Serif', 'Playfair Display', serif;
    font-size: 34px;
    font-weight: 900;
    letter-spacing: 1.2px;
    color: #FFFFFF;
    text-transform: uppercase;
    text-shadow: 0 2px 10px rgba(0,0,0,0.6);
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .date-pill {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 800;
    background: #0284C7;
    color: #FFF;
    padding: 3px 8px;
    border-radius: 4px;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .edition-tag {
    font-size: 10px;
    font-weight: 700;
    color: #38BDF8;
    letter-spacing: 1.2px;
    background: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.35);
    padding: 4px 10px;
    border-radius: 4px;
    text-transform: uppercase;
  }

  /* Rapid Alert Strip */
  .alert-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-top: 4px;
  }
  .alert-item {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 4px;
    padding: 3.5px 7px;
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 9.5px;
    font-weight: 700;
    color: #E2E8F0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .pulse-dot {
    width: 6.5px;
    height: 6.5px;
    border-radius: 50%;
    flex-shrink: 0;
  }
  .dot-red { background: #EF4444; box-shadow: 0 0 6px #EF4444; }
  .dot-amber { background: #F59E0B; box-shadow: 0 0 6px #F59E0B; }
  .dot-cyan { background: #06B6D4; box-shadow: 0 0 6px #06B6D4; }
  .dot-purple { background: #A855F7; box-shadow: 0 0 6px #A855F7; }

  /* Layout Grids */
  .grid-hero {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 8px;
    position: relative;
    z-index: 2;
  }

  .grid-three {
    display: grid;
    grid-template-columns: 1fr 1.08fr 1fr;
    gap: 10px;
    margin-top: 8px;
    position: relative;
    z-index: 2;
  }

  .grid-bottom {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
    margin-top: 8px;
    position: relative;
    z-index: 2;
  }

  /* News Card Styles */
  .news-card {
    background: rgba(16, 23, 38, 0.92);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 7px;
    padding: 9px 11px;
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
    height: 2.5px;
  }
  .card-red::after { background: #EF4444; }
  .card-emerald::after { background: #10B981; }
  .card-blue::after { background: #38BDF8; }
  .card-purple::after { background: #8B5CF6; }
  .card-teal::after { background: #14B8A6; }
  .card-amber::after { background: #F59E0B; }
  .card-gold::after { background: #EAB308; }
  .card-map::after { background: linear-gradient(90deg, #38BDF8, #818CF8, #C084FC); }

  .card-badge-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
  }
  .badge {
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 0.9px;
    text-transform: uppercase;
    padding: 2px 6px;
    border-radius: 3px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }
  .badge-red { background: rgba(239, 68, 68, 0.2); color: #FCA5A5; border: 1px solid rgba(239, 68, 68, 0.4); }
  .badge-emerald { background: rgba(16, 185, 129, 0.2); color: #6EE7B7; border: 1px solid rgba(16, 185, 129, 0.4); }
  .badge-blue { background: rgba(56, 189, 248, 0.2); color: #7DD3FC; border: 1px solid rgba(56, 189, 248, 0.4); }
  .badge-purple { background: rgba(139, 92, 246, 0.2); color: #C4B5FD; border: 1px solid rgba(139, 92, 246, 0.4); }
  .badge-teal { background: rgba(20, 184, 166, 0.2); color: #5EEAD4; border: 1px solid rgba(20, 184, 166, 0.4); }
  .badge-amber { background: rgba(245, 158, 11, 0.2); color: #FCD34D; border: 1px solid rgba(245, 158, 11, 0.4); }
  .badge-gold { background: rgba(234, 179, 8, 0.2); color: #FDE047; border: 1px solid rgba(234, 179, 8, 0.4); }

  .stat-pill {
    font-size: 8.5px;
    font-weight: 700;
    color: #94A3B8;
    background: rgba(255, 255, 255, 0.06);
    padding: 2px 5px;
    border-radius: 3px;
    letter-spacing: 0.5px;
  }

  .card-headline {
    font-size: 13.5px;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.25;
    margin-bottom: 5px;
    letter-spacing: -0.2px;
  }
  .card-headline.large {
    font-size: 15.5px;
    margin-bottom: 6px;
  }

  .card-content-layout {
    display: flex;
    gap: 9px;
    align-items: stretch;
  }
  .card-bullets {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .bullet-item {
    font-size: 11.5px;
    line-height: 1.36;
    color: #CBD5E1;
    position: relative;
    padding-left: 10px;
  }
  .bullet-item::before {
    content: "■";
    position: absolute;
    left: 0;
    top: 0;
    font-size: 6.5px;
    color: #64748B;
  }
  .bullet-item strong {
    color: #F8FAFC;
    font-weight: 750;
  }

  /* Bespoke Graphic Boxes for Every Card */
  .diagram-box {
    width: 114px;
    flex-shrink: 0;
    background: rgba(9, 14, 24, 0.92);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 5px;
    padding: 4px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
  }
  .diagram-box.compact {
    width: 86px;
  }
  .diagram-label {
    font-size: 8px;
    font-weight: 800;
    text-transform: uppercase;
    color: #94A3B8;
    margin-top: 2px;
    letter-spacing: 0.5px;
  }
  .diagram-val {
    font-size: 10.5px;
    font-weight: 800;
    color: #F8FAFC;
  }

  /* World Map Card */
  .map-card {
    background: rgba(11, 17, 29, 0.96);
    padding: 7px 9px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .map-container {
    width: 100%;
    height: 148px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  /* Bottom status strip in smaller cards */
  .mini-visual-strip {
    margin-top: 4px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2.5px 6px;
    border-radius: 3.5px;
    font-size: 8.5px;
    font-weight: 750;
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
  }
  .footer-bar span.accent {
    color: #F8FAFC;
    font-weight: 800;
  }
</style>
</head>
<body>
<div class="canvas">

  <!-- HEADER -->
  <div class="header-masthead">
    <div class="top-meta-row">
      <div class="pub-name">
        <span class="pub-badge">VERIFIED WIRE INTELLIGENCE</span>
        <span>THE GLOBAL CHRONICLE · INTERNATIONAL SITUATION REPORT</span>
      </div>
      <div>GLOBAL BRIEFING · ALL TIME ZONES</div>
      <div>SUNDAY EDITION</div>
    </div>

    <div class="headline-date-row">
      <div class="date-title">
        SUNDAY, 22 NOVEMBER 2026
        <span class="date-pill">WORLD EDITION</span>
      </div>
      <div class="edition-tag">SPECIAL CONSOLIDATED REPORT</div>
    </div>

    <!-- Alert Strip with 4 Key Flashpoints -->
    <div class="alert-strip">
      <div class="alert-item">
        <div class="pulse-dot dot-red"></div>
        <span>STRAIT OF HORMUZ: TANKERS HIT</span>
      </div>
      <div class="alert-item">
        <div class="pulse-dot dot-amber"></div>
        <span>COP31 ANTALYA: DAY 2 OVERTIME</span>
      </div>
      <div class="alert-item">
        <div class="pulse-dot dot-cyan"></div>
        <span>INDONESIA: M7.2 QUAKE (MALUKU)</span>
      </div>
      <div class="alert-item">
        <div class="pulse-dot dot-purple"></div>
        <span>VEGAS GP: VERSTAPPEN POLE (04:00 UTC)</span>
      </div>
    </div>
  </div>

  <!-- TIER 1: LEAD HERO CARDS (Middle East & COP31) -->
  <div class="grid-hero">
    
    <!-- MIDDLE EAST & GULF -->
    <div class="news-card card-red">
      <div>
        <div class="card-badge-row">
          <div class="badge badge-red">
            <svg width="9" height="9" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2L1 21h22L12 2zm0 3.8L20 19H4l8-13.2zM11 10h2v4h-2zm0 6h2v2h-2z"/></svg>
            MIDDLE EAST / GULF
          </div>
          <div class="stat-pill">RED ALERT · HORMUZ</div>
        </div>
        <div class="card-headline large">
          Bahrain Intercepts Drone Salvo; Tankers Hit Near Strait of Hormuz
        </div>
        <div class="card-content-layout">
          <div class="card-bullets">
            <div class="bullet-item"><strong>Bahrain Air Defense:</strong> Intercepts Iranian missile & drone salvo; falling debris sparks blaze at industrial facility.</div>
            <div class="bullet-item"><strong>Hormuz Tankers & CENTCOM:</strong> Commercial tankers hit in strategic waters; CENTCOM firmly refutes Iranian claims of a damaged F-16.</div>
            <div class="bullet-item"><strong>Tehran Talks & Gaza:</strong> Qatar mediates emergency talks in Tehran; displaced Gazans protest ongoing strikes near Yellow Line.</div>
          </div>
          <!-- Diagram: Hormuz Defense Radar -->
          <div class="diagram-box">
            <svg width="104" height="68" viewBox="0 0 104 68">
              <rect width="104" height="68" rx="4" fill="#0C1322"/>
              <!-- Radar sweep circles -->
              <circle cx="52" cy="36" r="28" fill="none" stroke="#EF4444" stroke-width="0.8" stroke-dasharray="2,2"/>
              <circle cx="52" cy="36" r="16" fill="none" stroke="#EF4444" stroke-width="0.8"/>
              <line x1="52" y1="8" x2="52" y2="64" stroke="#334155" stroke-width="0.8"/>
              <line x1="24" y1="36" x2="80" y2="36" stroke="#334155" stroke-width="0.8"/>
              <!-- Intercept Vector -->
              <path d="M 28 54 Q 52 20 74 27" fill="none" stroke="#F59E0B" stroke-width="1.8" stroke-dasharray="3,2"/>
              <circle cx="74" cy="27" r="3.5" fill="#EF4444"/>
              <circle cx="74" cy="27" r="6" fill="none" stroke="#EF4444" stroke-width="0.9"/>
              <text x="52" y="8" fill="#94A3B8" font-size="6" font-weight="700" text-anchor="middle">HORMUZ RADAR</text>
              <text x="74" y="21" fill="#F87171" font-size="5.5" font-weight="800" text-anchor="middle">INTERCEPT</text>
              <text x="30" y="60" fill="#FBBF24" font-size="5.5" font-weight="700">BAHRAIN</text>
              <text x="76" y="60" fill="#38BDF8" font-size="5.5" font-weight="700">IRAN</text>
            </svg>
            <div class="diagram-label">AIR DEFENSE · CENTCOM</div>
            <div class="diagram-val" style="color:#FCA5A5;">HIGH ALERT</div>
          </div>
        </div>
      </div>
    </div>

    <!-- CLIMATE / COP31 ANTALYA -->
    <div class="news-card card-emerald">
      <div>
        <div class="card-badge-row">
          <div class="badge badge-emerald">
            <svg width="9" height="9" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
            CLIMATE / UN SUMMIT
          </div>
          <div class="stat-pill">ANTALYA · ~200 NATIONS</div>
        </div>
        <div class="card-headline large">
          COP31 Stretches into Day 2 Overtime Clashing on Fossil Fuels
        </div>
        <div class="card-content-layout">
          <div class="card-bullets">
            <div class="bullet-item"><strong>Antalya Day 2 Overtime:</strong> UN COP31 climate negotiations push into a 2nd unscheduled overtime day on Nov 22.</div>
            <div class="bullet-item"><strong>~200 Nations Impasse:</strong> Petro-states and vulnerable nations deadlocked over fossil fuel phase-out and finance goals.</div>
            <div class="bullet-item"><strong>Third Draft Crisis:</strong> Delegations debate emergency 3rd draft text through the night to avoid summit collapse.</div>
          </div>
          <!-- Diagram: COP31 Status (Strict factual reporting, no invented numbers) -->
          <div class="diagram-box">
            <svg width="104" height="68" viewBox="0 0 104 68">
              <rect width="104" height="68" rx="4" fill="#0A1619"/>
              <text x="52" y="9" fill="#6EE7B7" font-size="6.5" font-weight="800" text-anchor="middle">COP31 TEXT STATUS</text>
              <!-- Factual Status Bars -->
              <rect x="8" y="16" width="88" height="12" rx="2" fill="#1E293B"/>
              <rect x="8" y="16" width="88" height="12" rx="2" fill="#0D9488"/>
              <text x="52" y="24.5" fill="#FFF" font-size="6.5" font-weight="800" text-anchor="middle">3RD DRAFT TEXT</text>
              <rect x="8" y="32" width="88" height="12" rx="2" fill="#F59E0B"/>
              <text x="52" y="40.5" fill="#000" font-size="6.5" font-weight="900" text-anchor="middle">DAY 2 OVERTIME</text>
              <!-- Two pills: 200 nations & Stalled -->
              <rect x="8" y="48" width="42" height="15" rx="2" fill="#334155"/>
              <text x="29" y="58" fill="#E2E8F0" font-size="6" font-weight="700" text-anchor="middle">~200 NATIONS</text>
              <rect x="54" y="48" width="42" height="15" rx="2" fill="#E11D48"/>
              <text x="75" y="58" fill="#FFF" font-size="6" font-weight="800" text-anchor="middle">STALLED</text>
            </svg>
            <div class="diagram-label">FOSSIL FUELS & FINANCE</div>
            <div class="diagram-val" style="color:#6EE7B7;">OVERTIME DAY 2</div>
          </div>
        </div>
      </div>
    </div>

  </div>

  <!-- TIER 2: EUROPE, WORLD RADAR MAP, UN GENEVA -->
  <div class="grid-three">
    
    <!-- EUROPE / BALTIC & NATO -->
    <div class="news-card card-blue">
      <div>
        <div class="card-badge-row">
          <div class="badge badge-blue">EUROPE / DEFENSE</div>
          <div class="stat-pill">BALTIC · NATO</div>
        </div>
        <div class="card-headline">
          Russian Ship Sparta II Hit; NATO Pledges Polish Defense
        </div>
        <div class="card-content-layout">
          <div class="card-bullets">
            <div class="bullet-item"><strong>Sparta II Drone Strike:</strong> Russian military cargo vessel ablaze in Gulf of Finland; 16 crew evacuated safely.</div>
            <div class="bullet-item"><strong>NATO Poland Vow:</strong> Sec-Gen Rutte pledges alliance will defend "every inch" of Poland after airspace violations.</div>
            <div class="bullet-item"><strong>Brussels Airport Alert:</strong> Preemptive Monday flight cancellations warned ahead of national ATC strike.</div>
          </div>
          <!-- Bespoke SVG: Ship fire + NATO Star with bold 10-12px text -->
          <div class="diagram-box compact">
            <svg width="78" height="66" viewBox="0 0 78 66">
              <rect width="78" height="66" rx="4" fill="#0B1526"/>
              <!-- NATO 4-point star -->
              <path d="M 20 16 L 23 9 L 26 16 L 33 19 L 26 22 L 23 29 L 20 22 L 13 19 Z" fill="#38BDF8"/>
              <!-- Cargo ship hull -->
              <path d="M 38 27 L 44 37 L 70 37 L 74 27 Z" fill="#475569"/>
              <rect x="48" y="19" width="10" height="8" fill="#64748B"/>
              <!-- Flames -->
              <path d="M 52 18 Q 55 10 58 17 Q 61 9 64 18 Z" fill="#EF4444"/>
              <path d="M 54 18 Q 56 12 58 17 Z" fill="#FBBF24"/>
              <!-- Bold clean labels -->
              <text x="39" y="50" fill="#F87171" font-size="10.5" font-weight="900" text-anchor="middle">SPARTA II</text>
              <text x="39" y="61" fill="#7DD3FC" font-size="9.5" font-weight="800" text-anchor="middle">16 RESCUED</text>
            </svg>
            <div class="diagram-label">GULF OF FINLAND</div>
          </div>
        </div>
      </div>
      <div class="mini-visual-strip" style="background:rgba(56,189,248,0.08); border:1px solid rgba(56,189,248,0.25);">
        <span style="color:#7DD3FC;">VESSEL SPARTA II ABLAZE</span>
        <span style="color:#94A3B8;">16 CREW EVACUATED</span>
      </div>
    </div>

    <!-- CENTRAL WORLD INCIDENT MAP -->
    <div class="news-card card-map map-card">
      <div class="card-badge-row">
        <div class="badge" style="background:rgba(99,102,241,0.22); color:#A5B4FC; border:1px solid rgba(99,102,241,0.45);">
          22 NOV GLOBAL MAP
        </div>
        <div class="stat-pill" style="color:#38BDF8;">8 MONITORED ZONES</div>
      </div>
      
      <!-- SVG World Map with ZERO Clipped Labels (all text-anchor carefully bounded) -->
      <div class="map-container">
        <svg width="298" height="142" viewBox="0 0 298 142">
          <!-- Background & Grid -->
          <rect width="298" height="142" rx="4" fill="#0A111E"/>
          <line x1="0" y1="48" x2="298" y2="48" stroke="#1E293B" stroke-width="0.7"/>
          <line x1="0" y1="94" x2="298" y2="94" stroke="#1E293B" stroke-width="0.7"/>
          <line x1="74" y1="0" x2="74" y2="142" stroke="#1E293B" stroke-width="0.7"/>
          <line x1="149" y1="0" x2="149" y2="142" stroke="#1E293B" stroke-width="0.7"/>
          <line x1="223" y1="0" x2="223" y2="142" stroke="#1E293B" stroke-width="0.7"/>

          <!-- High-Contrast World Continents -->
          <!-- North America -->
          <path d="M 28 26 L 56 22 L 72 32 L 64 50 L 48 64 L 42 58 L 26 46 Z" fill="#1C283C" stroke="#334A6E" stroke-width="0.9"/>
          <!-- South America -->
          <path d="M 54 70 L 76 74 L 72 104 L 60 124 L 50 100 Z" fill="#1C283C" stroke="#334A6E" stroke-width="0.9"/>
          <!-- Europe & UK -->
          <path d="M 124 26 L 152 24 L 150 42 L 132 46 L 126 36 Z" fill="#1C283C" stroke="#334A6E" stroke-width="0.9"/>
          <!-- Africa -->
          <path d="M 126 50 L 158 52 L 162 88 L 144 114 L 130 88 Z" fill="#1C283C" stroke="#334A6E" stroke-width="0.9"/>
          <!-- Asia -->
          <path d="M 154 22 L 238 22 L 248 48 L 212 66 L 180 62 L 162 42 Z" fill="#1C283C" stroke="#334A6E" stroke-width="0.9"/>
          <!-- Indonesia / Southeast Asia -->
          <path d="M 212 72 L 228 72 L 234 84 L 214 86 Z" fill="#1C283C" stroke="#334A6E" stroke-width="0.9"/>
          <!-- Australia -->
          <path d="M 226 94 L 258 94 L 254 120 L 230 118 Z" fill="#1C283C" stroke="#334A6E" stroke-width="0.9"/>

          <!-- Flashpoints with Short Crisp Labels & Zero Clipping (x safely between 14 and 284) -->
          <!-- 1. Florida -->
          <circle cx="60" cy="50" r="3.2" fill="#F59E0B"/>
          <line x1="60" y1="50" x2="48" y2="60" stroke="#F59E0B" stroke-width="0.7"/>
          <text x="14" y="68" fill="#FCD34D" font-size="7.5" font-weight="900" text-anchor="start">FLORIDA</text>

          <!-- 2. Las Vegas -->
          <circle cx="42" cy="38" r="3.2" fill="#EAB308"/>
          <line x1="42" y1="38" x2="34" y2="28" stroke="#EAB308" stroke-width="0.7"/>
          <text x="14" y="24" fill="#FDE047" font-size="7.5" font-weight="900" text-anchor="start">LAS VEGAS</text>

          <!-- 3. Baltic Sea -->
          <circle cx="146" cy="27" r="3.2" fill="#38BDF8"/>
          <line x1="146" y1="27" x2="146" y2="16" stroke="#38BDF8" stroke-width="0.7"/>
          <text x="146" y="13" fill="#7DD3FC" font-size="7.5" font-weight="900" text-anchor="middle">BALTIC</text>

          <!-- 4. Geneva -->
          <circle cx="134" cy="38" r="3" fill="#A855F7"/>
          <line x1="134" y1="38" x2="114" y2="38" stroke="#A855F7" stroke-width="0.7"/>
          <text x="110" y="41" fill="#C4B5FD" font-size="7.5" font-weight="900" text-anchor="end">GENEVA</text>

          <!-- 5. Antalya COP31 -->
          <circle cx="150" cy="45" r="3.2" fill="#10B981"/>
          <line x1="150" y1="45" x2="136" y2="56" stroke="#10B981" stroke-width="0.7"/>
          <text x="132" y="60" fill="#6EE7B7" font-size="7.5" font-weight="900" text-anchor="end">COP31</text>

          <!-- 6. Hormuz / Bahrain -->
          <circle cx="168" cy="56" r="3.5" fill="#EF4444"/>
          <line x1="168" y1="56" x2="180" y2="64" stroke="#EF4444" stroke-width="0.7"/>
          <text x="184" y="67" fill="#FCA5A5" font-size="7.5" font-weight="900" text-anchor="start">HORMUZ</text>

          <!-- 7. Maluku M7.2 Quake -->
          <circle cx="232" cy="80" r="3.5" fill="#14B8A6"/>
          <line x1="232" y1="80" x2="242" y2="88" stroke="#14B8A6" stroke-width="0.7"/>
          <text x="284" y="91" fill="#5EEAD4" font-size="7.5" font-weight="900" text-anchor="end">MALUKU M7.2</text>

          <!-- 8. Fukushima Blizzard -->
          <circle cx="242" cy="38" r="3" fill="#E2E8F0"/>
          <line x1="242" y1="38" x2="252" y2="28" stroke="#E2E8F0" stroke-width="0.7"/>
          <text x="284" y="27" fill="#FFFFFF" font-size="7.5" font-weight="900" text-anchor="end">FUKUSHIMA</text>
        </svg>
      </div>

      <div style="font-size:8px; text-align:center; color:#94A3B8; font-weight:700;">
        VERIFIED FLASHPOINTS · COORDINATES & REPORTS RECORDED NOV 22, 2026
      </div>
    </div>

    <!-- UN / GENEVA DISARMAMENT -->
    <div class="news-card card-purple">
      <div>
        <div class="card-badge-row">
          <div class="badge badge-purple">UN / GENEVA</div>
          <div class="stat-pill">DISARMAMENT</div>
        </div>
        <div class="card-headline">
          UN Fails on Autonomous Weapon Ban; Set to 2028
        </div>
        <div class="card-content-layout">
          <div class="card-bullets">
            <div class="bullet-item"><strong>No Killer Robot Ban:</strong> Geneva convention fails to agree on a legally binding treaty banning autonomous AI weapons.</div>
            <div class="bullet-item"><strong>Roadmap to 2028:</strong> States approve a 2-year consultation timetable extending talks through 2028.</div>
            <div class="bullet-item"><strong>Rights Groups Alarm:</strong> Monitors warn battlefield AI deployment is outpacing international regulations.</div>
          </div>
          <!-- Bespoke SVG: Autonomous drone crosshair + bold text -->
          <div class="diagram-box compact">
            <svg width="78" height="66" viewBox="0 0 78 66">
              <rect width="78" height="66" rx="4" fill="#150E22"/>
              <!-- Crosshair Circle -->
              <circle cx="39" cy="22" r="15" fill="none" stroke="#A855F7" stroke-width="1.2" stroke-dasharray="3,2"/>
              <line x1="39" y1="4" x2="39" y2="40" stroke="#8B5CF6" stroke-width="0.8"/>
              <line x1="21" y1="22" x2="57" y2="22" stroke="#8B5CF6" stroke-width="0.8"/>
              <!-- Drone Silhouette -->
              <path d="M 31 22 L 39 16 L 47 22 L 39 25 Z" fill="#C4B5FD"/>
              <circle cx="39" cy="22" r="2.8" fill="#EF4444"/>
              <!-- Bold clean labels -->
              <text x="39" y="50" fill="#F472B6" font-size="10.5" font-weight="900" text-anchor="middle">NO BAN</text>
              <text x="39" y="61" fill="#C4B5FD" font-size="9.5" font-weight="800" text-anchor="middle">ROADMAP 2028</text>
            </svg>
            <div class="diagram-label">LETHAL AI SYSTEMS</div>
          </div>
        </div>
      </div>
      <div class="mini-visual-strip" style="background:rgba(168,85,247,0.08); border:1px solid rgba(168,85,247,0.25);">
        <span style="color:#C4B5FD;">AUTONOMOUS WEAPONS</span>
        <span style="color:#F472B6;">2-YEAR PROCESS TO 2028</span>
      </div>
    </div>

  </div>

  <!-- TIER 3: ASIA-PACIFIC, AMERICAS WEATHER, GLOBAL SPORT -->
  <div class="grid-bottom">
    
    <!-- ASIA-PACIFIC -->
    <div class="news-card card-teal">
      <div>
        <div class="card-badge-row">
          <div class="badge badge-teal">ASIA-PACIFIC</div>
          <div class="stat-pill">QUAKE · ICJ · BLIZZARD</div>
        </div>
        <div class="card-headline">
          M7.2 Quake Off Maluku; ICJ Finds Myanmar Genocide
        </div>
        <div class="card-content-layout">
          <div class="card-bullets">
            <div class="bullet-item"><strong>M7.2 Maluku Quake:</strong> Major 7.2 earthquake strikes off Indonesia; agencies confirm no tsunami threat.</div>
            <div class="bullet-item"><strong>ICJ Genocide Verdict:</strong> World Court rules Myanmar committed genocide against the Rohingya.</div>
            <div class="bullet-item"><strong>Fukushima Blizzard:</strong> Severe heavy mountain snow isolates 1,000+ residents in Japan.</div>
          </div>
          <!-- Bespoke SVG: Seismic rings + ICJ Gavel with 10-12px bold text -->
          <div class="diagram-box compact">
            <svg width="78" height="66" viewBox="0 0 78 66">
              <rect width="78" height="66" rx="4" fill="#0A181A"/>
              <!-- Seismograph pulse circles -->
              <circle cx="39" cy="20" r="5" fill="#14B8A6" fill-opacity="0.3"/>
              <circle cx="39" cy="20" r="11" fill="none" stroke="#14B8A6" stroke-width="1.1" stroke-dasharray="2,2"/>
              <circle cx="39" cy="20" r="16" fill="none" stroke="#2DD4BF" stroke-width="0.9"/>
              <text x="39" y="24" fill="#FFFFFF" font-size="12" font-weight="900" text-anchor="middle">M7.2</text>
              <!-- Bold clean labels -->
              <text x="39" y="50" fill="#5EEAD4" font-size="10.5" font-weight="900" text-anchor="middle">ICJ GUILTY</text>
              <text x="39" y="61" fill="#94A3B8" font-size="9" font-weight="800" text-anchor="middle">NO TSUNAMI</text>
            </svg>
            <div class="diagram-label">SEISMIC & LEGAL</div>
          </div>
        </div>
      </div>
      <div class="mini-visual-strip" style="background:rgba(20,184,166,0.08); border:1px solid rgba(20,184,166,0.25);">
        <span style="color:#5EEAD4;">INDONESIA M7.2 QUAKE</span>
        <span style="color:#E2E8F0;">ROHINGYA GENOCIDE RULING</span>
      </div>
    </div>

    <!-- AMERICAS / WEATHER -->
    <div class="news-card card-amber">
      <div>
        <div class="card-badge-row">
          <div class="badge badge-amber">AMERICAS / WEATHER</div>
          <div class="stat-pill">FLORIDA INUNDATION</div>
        </div>
        <div class="card-headline">
          Historic St. Johns River Floods Trigger Evacuations
        </div>
        <div class="card-content-layout">
          <div class="card-bullets">
            <div class="bullet-item"><strong>Record Flood Crests:</strong> Storms swell Florida's St. Johns River to historic flood stage, inundating low basins.</div>
            <div class="bullet-item"><strong>Evacuations Urged:</strong> Emergency authorities issue evacuation warnings across low-lying river counties.</div>
            <div class="bullet-item"><strong>Infrastructure Inundated:</strong> High waters breach roads and submerge residential riverfront communities.</div>
          </div>
          <!-- Bespoke SVG: River Flood Surge Gauge with bold text -->
          <div class="diagram-box compact">
            <svg width="78" height="66" viewBox="0 0 78 66">
              <rect width="78" height="66" rx="4" fill="#1C1408"/>
              <!-- Water Gauge -->
              <rect x="18" y="10" width="10" height="24" rx="2" fill="#334155"/>
              <rect x="18" y="16" width="10" height="18" rx="2" fill="#F59E0B"/>
              <!-- Warning Triangle -->
              <path d="M 52 10 L 64 26 L 40 26 Z" fill="#EF4444"/>
              <text x="52" y="23" fill="#FFF" font-size="8" font-weight="900" text-anchor="middle">!</text>
              <!-- Bold clean labels -->
              <text x="39" y="50" fill="#FCD34D" font-size="10.5" font-weight="900" text-anchor="middle">ST. JOHNS</text>
              <text x="39" y="61" fill="#F87171" font-size="9.5" font-weight="900" text-anchor="middle">EVACUATE</text>
            </svg>
            <div class="diagram-label">RIVER HYDROLOGY</div>
          </div>
        </div>
      </div>
      <div class="mini-visual-strip" style="background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.25);">
        <span style="color:#FCD34D;">ST. JOHNS RIVER SURGE</span>
        <span style="color:#EF4444;">EVACUATION WARNINGS</span>
      </div>
    </div>

    <!-- GLOBAL SPORT -->
    <div class="news-card card-gold">
      <div>
        <div class="card-badge-row">
          <div class="badge badge-gold">GLOBAL SPORT</div>
          <div class="stat-pill">F1 VEGAS · ATP FINALS</div>
        </div>
        <div class="card-headline">
          Verstappen on Pole in Vegas; Alcaraz vs Zverev in Turin
        </div>
        <div class="card-content-layout">
          <div class="card-bullets">
            <div class="bullet-item"><strong>Verstappen Vegas Pole:</strong> Max Verstappen qualifies P1 ahead of George Russell for Las Vegas GP (04:00 UTC).</div>
            <div class="bullet-item"><strong>Antonelli Grid Penalty:</strong> Champion Kimi Antonelli drops from front row to P6 following penalty.</div>
            <div class="bullet-item"><strong>ATP Finals Title Match:</strong> Carlos Alcaraz takes on Alexander Zverev in premier championship match.</div>
          </div>
          <!-- Bespoke SVG: F1 Checkered flag + Trophy with bold text -->
          <div class="diagram-box compact">
            <svg width="78" height="66" viewBox="0 0 78 66">
              <rect width="78" height="66" rx="4" fill="#1C1808"/>
              <!-- Checkered pattern -->
              <rect x="14" y="10" width="7" height="7" fill="#FFF"/>
              <rect x="21" y="10" width="7" height="7" fill="#333"/>
              <rect x="14" y="17" width="7" height="7" fill="#333"/>
              <rect x="21" y="17" width="7" height="7" fill="#FFF"/>
              <!-- Trophy -->
              <path d="M 46 10 L 58 10 L 56 22 Q 52 28 46 28 Z" fill="#FDE047"/>
              <rect x="49" y="28" width="4" height="6" fill="#EAB308"/>
              <!-- Bold clean labels with generous margins -->
              <text x="39" y="41" fill="#FDE047" font-size="11" font-weight="900" text-anchor="middle">P1 VER</text>
              <text x="39" y="52" fill="#A7F3D0" font-size="9" font-weight="800" text-anchor="middle">ALCARAZ</text>
              <text x="39" y="61" fill="#94A3B8" font-size="8.5" font-weight="800" text-anchor="middle">VS ZVEREV</text>
            </svg>
            <div class="diagram-label">MOTORSPORT & TENNIS</div>
          </div>
        </div>
      </div>
      <div class="mini-visual-strip" style="background:rgba(234,179,8,0.08); border:1px solid rgba(234,179,8,0.25);">
        <span style="color:#FDE047;">F1 VEGAS POLE (04:00 UTC)</span>
        <span style="color:#A7F3D0;">ATP FINALS CHAMPIONSHIP</span>
      </div>
    </div>

  </div>

  <!-- EDITORIAL DATELINE FOOTER (Strictly single line) -->
  <div class="footer-bar">
    <div>WORLD NEWS SUMMARY · <span class="accent">SUNDAY, 22 NOVEMBER 2026</span></div>
    <div><span class="accent">7 REGIONS</span> · VERIFIED WIRE REPORTS</div>
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
                if os.path.islink(fpath) or os.path.isfile(fpath):
                    os.unlink(fpath)
            except OSError:
                pass

    if os.path.exists(TMP_PNG):
        os.remove(TMP_PNG)

    print("[*] Launching headless Chrome screenshot with host isolation...")
    os.system(f"rm -f {TMP_PROFILE}/Singleton*")
    chrome_cmd = (
        f"google-chrome "
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
        print(f"[!] Chrome command failed, log output:")
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
