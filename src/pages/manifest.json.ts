import type { APIRoute, ImageMetadata } from "astro";
import { getImage } from "astro:assets";
import nutriwattLogoWithName from "@images/nutriwatt-logo-with-name.png";
// Utiliser le logo Nutriwatt avec nom pour les icônes
const icon = nutriwattLogoWithName;
const maskableIcon = nutriwattLogoWithName;

interface Favicon {
  purpose: 'any' | 'maskable' | 'monochrome';
  src: ImageMetadata;
  sizes: number[];
}

const sizes = [192, 512];
const favicons: Favicon[] = [
  {
    purpose: 'any',
    src: icon,
    sizes,
  },
  {
    purpose: 'maskable',
    src: maskableIcon,
    sizes,
   },
];

export const GET: APIRoute = async () => {
  const icons = await Promise.all(
    favicons.flatMap((favicon) =>
      favicon.sizes.map(async (size) => {
        const image = await getImage({
          src: favicon.src,
          width: size,
          height: size,
          format: "png",
        });
        return {
          src: image.src,
          sizes: `${image.options.width}x${image.options.height}`,
          type: `image/${image.options.format}`,
          purpose: favicon.purpose,
        };
      }),
    ),
  );

  const manifest = {
    short_name: "Nutriwatt",
    name: "Nutriwatt - Health & Nutrition Tracking",
    icons,
    display: "minimal-ui",
    id: "/",
    start_url: "/",
    theme_color: "#3A73C1", // Bleu principal
    background_color: "#F4F4F4", // Blanc cassé
  };

  return new Response(JSON.stringify(manifest));
};
