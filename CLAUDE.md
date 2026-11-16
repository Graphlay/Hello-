# AI Video Editing Workspace

This repo is my video editing workspace. Read this first in every session so you know where files live and how I like videos edited.

## Where everything lives

| Folder           | Contents                                                         | Rules |
|------------------|------------------------------------------------------------------|-------|
| `raw-videos/`    | Original, unedited footage                                       | **Read-only.** Never modify, rename or delete. |
| `references/`    | Scripts, briefs, shot lists, "match this" examples for a project | Check here before starting any edit. |
| `inspirations/`  | General style inspiration (reels, transitions, grades, captions) | Use for creative direction. |
| `brand-kit/`     | Logos, colours, intro/outro, caption style, tone of voice        | Every edit must follow this. One sub-folder per brand/client. |
| `assets/music/`  | Licensed / royalty-free background tracks                        | Only use tracks listed as licensed. |
| `assets/sfx/`    | Sound effects                                                    | |
| `assets/images/` | Overlays, stickers, stills, textures                             | |
| `assets/fonts/`  | Font files                                                       | |
| `skills/`        | Reusable editing workflows (`<skill>/SKILL.md`)                  | Check for a matching skill before improvising. |
| `projects/`      | One folder per video: `brief.md`, `edit-notes.md`, `working/`, `captions/` | All work-in-progress goes here. |
| `exports/`       | Final renders only                                               | Never overwrite — bump the version. |

## Workflow

1. **Start a project:** create `projects/YYYY-MM-DD_project-name/` with a `brief.md` (goal, platform, target length, brand, deadline).
2. **Gather:** pull footage from `raw-videos/`, check `references/`, `brand-kit/` and relevant `skills/`.
3. **Edit:** keep intermediate files in the project's `working/` folder. Log decisions and feedback in `edit-notes.md`.
4. **Export:** render to `exports/` as `YYYY-MM-DD_project-name_platform_vNN.mp4`.
5. **Summarise:** tell me what changed, the export path, and anything that needs my decision.

## How I like my videos edited (defaults — override per project in `brief.md`)

- **Format:** vertical 9:16, 1080×1920, 30 fps unless the brief says otherwise (16:9 for YouTube).
- **Hook first:** the strongest moment or line in the first 1–3 seconds. No slow intros.
- **Pacing:** tight cuts — remove silences, ums, false starts and dead air. Keep it moving.
- **Captions:** always on, burned in, large and readable, brand font, key words highlighted in brand colour, kept inside safe zones (away from the platform UI at top/bottom).
- **Audio:** voice is clear and on top; music ducked under speech (around −18 to −22 dB under voice); loudness ≈ −14 LUFS for social.
- **SFX:** subtle — whooshes on transitions, pops on text/graphics. Never overpowering.
- **Colour:** natural, clean, flattering skin tones; consistent across clips.
- **Branding:** logo/watermark and outro/CTA from `brand-kit/`; colours and fonts from the brand kit only.
- **Language:** match the language of the footage/brief (English, Hindi or Hinglish captions as appropriate).
- **Export:** H.264 MP4, AAC audio, high bitrate; also export a thumbnail frame when useful.

## Rules for Claude

- Never touch originals in `raw-videos/`; work on copies.
- Never overwrite anything in `exports/`; create a new version.
- Only use music/fonts/assets that are in this workspace (or clearly licensed).
- If a brief is missing key info (platform, length, brand), ask before a long edit.
- Large media files are git-ignored (see `.gitignore`); only notes, briefs, captions and READMEs are committed.

> Edit the "How I like my videos edited" section anytime — it's my standing style guide.
