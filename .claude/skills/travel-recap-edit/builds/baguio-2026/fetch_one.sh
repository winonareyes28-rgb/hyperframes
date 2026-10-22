#!/bin/bash
# fetch_one.sh <day> <title> <id> <mime>
W=$(dirname "$0"); mkdir -p "$W/raw" "$W/proxy" "$W/photos" "$W/songs" "$W/meta"; day=$1; title=$2; id=$3; mime=$4
base="${title%.*}"; url="https://drive.usercontent.google.com/download?id=$id&export=download&confirm=t"
if [[ $mime == video/* ]]; then
  out=$W/proxy/${day}_${base}.mp4; [ -s "$out" ] && exit 0
  raw=$W/raw/${day}_$title
  for i in 1 2 3; do curl -sSL --retry 3 -o "$raw" "$url" && break; sleep 3; done
  ffprobe -v error -show_entries stream=codec_type,width,height,r_frame_rate,avg_frame_rate:stream_side_data=rotation:format=duration:format_tags=creation_time,com.apple.quicktime.creationdate -of json "$raw" > "$W/meta/${day}_${base}.json"
  # 1080-short-side proxy, 30fps, keep audio for possible reaction moments
  ffmpeg -nostdin -v error -y -i "$raw" -vf "scale='if(gt(iw,ih),-2,1080)':'if(gt(iw,ih),1080,-2)':flags=lanczos,fps=30,format=yuv420p" -c:v libx264 -preset veryfast -crf 18 -c:a aac -b:a 128k "$out.tmp.mp4" && mv "$out.tmp.mp4" "$out"
  # keep high-fps originals for slow-mo, drop the rest
  fps=$(jq -r '[.streams[]|select(.codec_type=="video")][0].avg_frame_rate' "$W/meta/${day}_${base}.json" | awk -F/ '{printf "%d", $1/($2?$2:1)}')
  if [ "${fps:-30}" -ge 100 ]; then ffmpeg -nostdin -v error -y -i "$raw" -vf "scale='if(gt(iw,ih),-2,1080)':'if(gt(iw,ih),1080,-2)'" -c:v libx264 -preset veryfast -crf 18 -an $W/proxy/${day}_${base}_hfr.mp4; fi
  rm -f "$raw"
elif [[ $mime == audio/* ]]; then
  curl -sSL --retry 3 -o "$W/songs/$title" "$url"
else
  out=$W/photos/${day}_${base}.jpg; [ -s "$out" ] && exit 0
  raw=$W/raw/${day}_$title; curl -sSL --retry 3 -o "$raw" "$url"
  python3 - "$raw" "$out" <<'PY'
import sys, pillow_heif
from PIL import Image, ImageOps
pillow_heif.register_heif_opener()
im = ImageOps.exif_transpose(Image.open(sys.argv[1])).convert('RGB')
im.thumbnail((2160, 2160), Image.LANCZOS); im.save(sys.argv[2], quality=92)
PY
  rm -f "$raw"
fi
