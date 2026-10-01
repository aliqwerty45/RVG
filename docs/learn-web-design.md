# Learning Web Design — a roadmap built around RVG

You already have the single best thing a beginner can have: **a real UI you care about.**
`pages.py` contains ~390 KB of hand-written HTML, CSS and vanilla JS (login page,
dashboard, public subscription page). That is your textbook *and* your lab.

This guide is a path from "I can change a colour" to "I can design a screen from
scratch", with every exercise anchored in this repo.

---

## 0. Set up the lab (2 minutes)

```bash
python3 devtools/design_playground.py
# → http://localhost:7100
```

It serves `pages.py` with **no backend, no login, no database**, and reloads the
browser every time you save the file. Routes:

| Route | What it renders | Good for learning |
|---|---|---|
| `/login` | `LOGIN_HTML` (~330 lines) | colour, typography, forms, centering |
| `/dashboard` | `DASHBOARD_HTML` (~5,300 lines) | layout, grids, tables, modals, state |
| `/sub` | `get_public_page_html()` | cards, progress bars, mobile-first |

Also open **DevTools** (F12). The Elements panel lets you edit CSS live without
touching the file — change, see, then port the winning value into `pages.py`.
90% of learning web design is this loop: *tweak → look → keep or undo.*

---

## 1. The four things "web design" actually is

Don't try to learn them at once. In order of payoff:

1. **Visual design** — colour, type, spacing, hierarchy. *The part that makes
   people say "this looks professional."* Mostly rules, learnable in weeks.
2. **CSS craft** — flexbox, grid, responsive units, transitions. The tool that
   executes the above.
3. **Interaction / UX** — states (hover, focus, loading, empty, error), feedback,
   information architecture.
4. **Systems** — design tokens, components, consistency at scale. You are
   *already* doing this: look at the `:root { --accent; --radius; --shadow }`
   block at the top of each page. Those are design tokens.

---

## 2. Phase 1 — Visual fundamentals (week 1–2)

### The five rules that fix most amateur UI

1. **Spacing on a scale.** Pick 4px steps: 4, 8, 12, 16, 24, 32, 48, 64. Never
   `padding: 13px`. Consistency reads as "designed".
2. **Two font sizes are not enough, seven are too many.** Use ~5: 12 / 14 / 16 / 20 / 28.
   Weight (500 vs 800) carries more hierarchy than size does.
3. **One accent colour.** Everything else is a neutral grey ramp. RVG does this
   well already: `--accent` + `--text/--dim/--mid`.
4. **Contrast is non-negotiable.** Body text needs ≥ 4.5:1 against its
   background. Check with DevTools' contrast tool — your `--dim: #5A6690` on
   `--bg: #080B14` is borderline for small text. That's a real bug to fix.
5. **Alignment.** Fewer alignment edges = calmer screen. Left-align (or in RTL,
   right-align) everything to the same invisible line.

### Exercises in this repo

- In `LOGIN_HTML`, change `--accent` to `#E0724F` (warm orange). Note that the
  glow, buttons and focus rings all follow — that's why tokens matter.
- Replace every hard-coded `border-radius` in the login card with
  `var(--radius)` and then try `--radius: 4px` vs `24px`.
- Audit the login page's spacing: list every padding/margin value, then snap
  each to the 4px scale.

### Resources (free, worth the time)

- **Refactoring UI** (book, paid — the single best beginner→good jump). Free
  substitute: the authors' [Twitter threads](https://www.refactoringui.com/).
- [Learn CSS — web.dev](https://web.dev/learn/css/) — the best structured CSS course.
- [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS) — your dictionary.
- [Practical Typography](https://practicaltypography.com/) — read "Summary of Key Rules".
- [Coolors](https://coolors.co/) / [Radix Colors](https://www.radix-ui.com/colors) for palettes that already work.

---

## 3. Phase 2 — CSS you must own (week 2–4)

| Topic | Why | Practice here |
|---|---|---|
| Box model, `box-sizing` | Everything sizes wrong until you get this | `*{box-sizing:border-box}` at the top of `pages.py` — remove it, see the chaos, put it back |
| Flexbox | 80% of layouts | Every `.top`, `.brand`, `.top-actions` in `get_public_page_html()` |
| Grid | Dashboards specifically | The dashboard's card grids |
| Custom properties | Theming | The `:root` / `[data-theme="light"]` pair — that's a whole dark/light theme in 20 lines |
| Media queries | Mobile | Grep `@media` in `pages.py`, then test at 375px |
| Transitions | Polish | `transition:.18s` on `.icon-btn` — try `cubic-bezier(.4,0,.2,1)` |
| Pseudo-elements | Decoration without extra markup | `.sub-info::before` radial glow |

**Drills:** [Flexbox Froggy](https://flexboxfroggy.com/), [Grid Garden](https://cssgridgarden.com/),
then [CSS Battle](https://cssbattle.dev/) when you want to show off.

**Exercise:** rebuild the public sub page's header (`.top` / `.brand` / `.top-actions`)
from a blank file, from memory. Recall beats re-reading.

---

## 4. Phase 3 — Responsive & RTL (week 4–5)

Your UI is Persian and `dir="rtl"` — you get to learn something most Western
tutorials skip, and it will make you better:

- Use **logical properties**: `margin-inline-start` instead of `margin-left`,
  `padding-inline`, `inset-inline-end`. They flip automatically between RTL and LTR.
- Mirror icons that imply direction (arrows), never mirror logos or numbers.
- Test both: add `dir="ltr"` temporarily in the playground and see what breaks.

Responsive checklist for every screen you build:
- 375px (phone), 768px (tablet), 1440px (desktop)
- No horizontal scroll at any width
- Tap targets ≥ 44×44px
- Text never below 14px on mobile

**Exercise:** open `/dashboard` at 375px in device mode. Write down the five
worst problems, then fix two of them with `flex-wrap` and one media query.

---

## 5. Phase 4 — Interaction & the states people forget (week 5–6)

For every component, design **five** states, not one:

1. default 2. hover/active 3. **focus-visible** (keyboard!) 4. loading 5. empty/error

Most "unfinished-feeling" UIs are missing 3, 4 and 5.

**Exercises:**
- Add a visible `:focus-visible` ring to every button in `LOGIN_HTML`, then
  navigate the whole page with Tab only.
- Add a skeleton/spinner state to one dashboard card while its `fetch()` resolves.
- Design the empty state for a dashboard list with zero items: icon + one line
  of explanation + one action button.

Accessibility minimum (it is design, not extra): real `<button>` elements,
`<label>` tied to every input, `alt` on images, visible focus, 4.5:1 contrast.

---

## 6. Phase 5 — Design systems & tooling (week 6+)

- Extract your tokens: colours, spacing scale, radii, shadows, type scale —
  write them once, use them everywhere. (`pages.py` is already 70% there.)
- Learn **one** framework only after the fundamentals: **Tailwind CSS** fits
  your style (utility classes, tokens built in) and is the industry default.
- Learn **Figma** basics (frames, auto-layout, components) — one weekend is
  enough to be useful; you'll design faster than you can code.
- Then, if you want interactive UIs: React/Next.js + a component library
  (shadcn/ui, Radix). But don't start here — people who skip CSS fundamentals
  stay stuck at "it works but looks off" for years.

---

## 7. How to actually get good (the meta part)

- **Copy, deliberately.** Pick a screen you admire ([Mobbin](https://mobbin.com/),
  [Dribbble](https://dribbble.com/), [Godly](https://godly.website/), Linear, Stripe,
  Vercel) and rebuild it pixel-close in plain HTML/CSS. You learn more in one
  clone than in ten tutorials.
- **Ship small, often.** 30 minutes a day beats a 6-hour Sunday.
- **Keep a swipe file.** Screenshot UI you like; note *why* in one sentence.
- **Get critique.** r/web_design, Designer Hangout, or just post before/after.
- **Redesign what you own.** Every improvement you make to RVG's dashboard is
  portfolio material and a real user (you) benefits.

### A concrete 8-week plan

| Week | Focus | Deliverable |
|---|---|---|
| 1 | Colour, type, spacing rules | Restyle `LOGIN_HTML` with a new palette + 4px scale |
| 2 | Flexbox + box model | Rebuild the sub-page header from scratch |
| 3 | Grid + responsive | Dashboard usable at 375px with no horizontal scroll |
| 4 | Tokens + theming | Clean, documented `:root` token block for all three pages |
| 5 | States & accessibility | Focus rings, loading and empty states everywhere |
| 6 | Clone study | Pixel-close clone of one screen you admire |
| 7 | Tailwind | Rebuild the login page in Tailwind |
| 8 | Figma → code | Design a new RVG page in Figma, then build it |

---

## 8. Quick reference — cheat values that usually look good

```css
/* spacing */      4 8 12 16 24 32 48 64 96
/* radius */       6px (tight) · 12px (default) · 20px (soft) · 999px (pill)
/* shadow */       0 1px 2px rgba(0,0,0,.06), 0 8px 24px rgba(0,0,0,.08)
/* transition */   .18s cubic-bezier(.4,0,.2,1)
/* line-height */  1.2 headings · 1.5–1.65 body
/* max width */    60–75 characters for readable text
/* grey ramp */    build from one hue, vary lightness only
```

---

## خلاصه فارسی

- با `python3 devtools/design_playground.py` رابط کاربری پروژه خودت را بدون بک‌اند و لاگین ببین؛ هر بار `pages.py` را ذخیره کنی، صفحه خودکار رفرش می‌شود.
- اول اصول بصری: فاصله‌گذاری روی مقیاس ۴ پیکسلی، حداکثر ۵ اندازه فونت، یک رنگ تأکیدی، کنتراست کافی.
- بعد CSS: فلکس‌باکس، گرید، متغیرهای CSS، مدیا کوئری.
- چون پروژه راست‌چین است، از ویژگی‌های منطقی مثل `margin-inline-start` استفاده کن.
- برای هر کامپوننت پنج حالت طراحی کن: عادی، هاور، فوکوس، در حال بارگذاری، خالی/خطا.
- بهترین تمرین: همین داشبورد RVG را هفته به هفته بازطراحی کن.
