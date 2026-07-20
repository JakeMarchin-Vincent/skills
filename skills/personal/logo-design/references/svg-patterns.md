# SVG Patterns — Copy-Paste Building Blocks

These are the techniques the five reference logos actually use. Reach for one of these before inventing anything new.

## 1. Mask to punch negative space (Margin pattern)

Use when you want a shape with a hole or line cut out of it.

```svg
<svg viewBox="0 0 80 80" fill="none">
  <defs>
    <mask id="cut">
      <rect x="0" y="0" width="80" height="80" fill="white" />
      <!-- whatever is black gets subtracted -->
      <rect x="20" y="12" width="3" height="56" fill="black" />
    </mask>
  </defs>
  <rect x="8" y="4" width="56" height="72" rx="4"
        fill="currentColor" mask="url(#cut)" />
</svg>
```

## 2. Arc as a bite out of a shape (Daylight pattern)

The `A rx ry x-axis-rotation large-arc sweep x y` path command cuts an arc between two points. Use it to carve a crescent / rounded bite.

```svg
<path d="M68 20
         L380 20
         Q400 20 400 68
         L400 332
         Q400 380 332 380
         L68 380
         Q20 380 20 332
         L20 180
         A160 160 0 0 0 180 20
         Z" fill="currentColor" />
```

The `A 160 160 0 0 0 180 20` is the bite — a 160-radius arc from the current point up to `(180, 20)`.

## 3. Zig-zag edge with a rounded body (Takeout pattern)

Alternate `L x y` commands with alternating up/down y-values to make teeth, then close with `Q` curves for rounded bottom corners.

```svg
<path d="M15 20 L20 15 L25 20 L30 15 L35 20 L40 15
         L45 20 L50 15 L55 20 L60 15 L65 20
         L65 60 Q65 65 60 65 L20 65 Q15 65 15 60 Z"
      fill="currentColor" />
```

## 4. Stacked rects with narrowing widths (Sift pattern)

Three `<rect>` elements with progressively smaller widths, centered by increasing `x`.

```svg
<svg viewBox="0 0 48 33" fill="none">
  <rect x="0"  y="0"  width="48" height="7" rx="2" fill="currentColor" />
  <rect x="8"  y="13" width="32" height="7" rx="2" fill="currentColor" />
  <rect x="16" y="26" width="16" height="7" rx="2" fill="currentColor" />
</svg>
```

## 5. Lines with primary/tint hierarchy (Aria pattern)

Use a stronger color for the "hero" element and a lighter tint for the supporting elements to create quiet hierarchy.

```svg
<svg viewBox="0 0 64 64" fill="none">
  <line x1="10" y1="18" x2="40" y2="18"
        class="stroke-primary-300 dark:stroke-primary-700"
        stroke-width="4" stroke-linecap="round" />
  <line x1="10" y1="32" x2="54" y2="32"
        class="stroke-primary-500"
        stroke-width="5" stroke-linecap="round" />
  <line x1="10" y1="46" x2="34" y2="46"
        class="stroke-primary-300 dark:stroke-primary-700"
        stroke-width="4" stroke-linecap="round" />
</svg>
```

## 6. Theming: currentColor vs Tailwind classes

**`currentColor`** — simplest, works anywhere. The SVG inherits whatever `color` the parent has.

```svg
<svg><path d="..." fill="currentColor" /></svg>
```

```vue
<LogoMark class="text-primary" />         <!-- primary color -->
<LogoMark class="text-white" />           <!-- reversed -->
```

**Tailwind classes** — use when you need per-element color or dark-mode variants.

```svg
<rect class="fill-sky-500 dark:fill-sky-400" />
```

Pick one approach per logo. Don't mix `fill="currentColor"` and hardcoded classes in the same mark.

## 7. Vue component wrapper (Nuxt / Nuxt UI)

Every project in Kyle's workspace uses the same pattern: a `LogoMark` component for the icon and an `AppLogo` component that pairs mark + wordmark.

```vue
<!-- LogoMark.vue -->
<script setup lang="ts">
withDefaults(defineProps<{
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
}>(), { size: 'md' })

const iconSize = {
  xs: 'size-4', sm: 'size-5', md: 'size-6', lg: 'size-8', xl: 'size-10'
}
</script>

<template>
  <svg :class="iconSize[size]" viewBox="0 0 64 64" fill="none" aria-hidden="true">
    <!-- paste the mark paths here -->
  </svg>
</template>
```

```vue
<!-- AppLogo.vue -->
<script setup lang="ts">
withDefaults(defineProps<{
  wordmark?: boolean
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
}>(), { wordmark: true, size: 'md' })

const textSize = {
  xs: 'text-sm', sm: 'text-base', md: 'text-xl', lg: 'text-2xl', xl: 'text-3xl'
}
const gapSize = {
  xs: 'gap-1', sm: 'gap-1.5', md: 'gap-2', lg: 'gap-2.5', xl: 'gap-3'
}
</script>

<template>
  <div :class="['flex items-center', wordmark && gapSize[size]]">
    <LogoMark :size class="text-primary" />
    <span v-if="wordmark"
          :class="[textSize[size], 'font-semibold tracking-tight text-highlighted leading-none']">
      BrandName
    </span>
  </div>
</template>
```

## 8. Favicon generation

For a Nuxt project, drop the standalone mark SVG at `public/favicon.svg` with a hardcoded fill so it renders correctly when loaded as a favicon (no CSS context).

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
  <path d="..." fill="#0ea5e9" />  <!-- hardcoded -->
</svg>
```

Keep the hardcoded-fill favicon *separate* from the themed component version. The component uses `currentColor`; the favicon uses a literal hex.
