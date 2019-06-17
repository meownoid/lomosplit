import argparse
import os
import sys

import skimage.io

from lomosplit.image import process_batch
from lomosplit.utils import get_grouped_images


def main():
    parser = argparse.ArgumentParser(
        description='Splits LomoKino film scans'
    )

    parser.add_argument(
        'input_folder',
        help='Input folder with scans to process'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        dest='quiet',
        help='Do not print anything'
    )

    parser.add_argument(
        '-o', '--output',
        action='store',
        dest='output_folder',
        default=None,
        help='Output folder to store results'
    )

    parser.add_argument(
        '--template',
        action='store',
        dest='frame_template',
        default='frame_{idx:d}',
        help='Frame filename template without extension'
    )

    parser.add_argument(
        '--format',
        action='store',
        dest='frame_format',
        default='jpg',
        help='Frame format (jpg, jpeg or png)'
    )

    parser.add_argument(
        '--luminosity-percentile',
        action='store',
        dest='luminosity_percentile',
        type=int,
        default=10,
        help='Luminosity percentile used to split frames'
    )

    parser.add_argument(
        '--rotate-image',
        action='store',
        dest='rotate_image',
        default='auto',
        help='Rotate image before processing (left, right or auto)'
    )

    parser.add_argument(
        '--rotate-frame',
        action='store',
        dest='rotate_frame',
        default='auto',
        help='Rotate frame before processing (left, right or auto)'
    )

    parser.add_argument(
        '--frame-min-height',
        action='store',
        dest='frame_min_height',
        default=None,
        help='Minimal frame height'
    )

    parser.add_argument(
        '--frame-max-height',
        action='store',
        dest='frame_max_height',
        default=None,
        help='Maximal frame height'
    )

    parser.add_argument(
        '--adjust-to-max-height',
        action='store_true',
        dest='adjust_to_max_height',
        help='Adjust each frame to maximum frame height (per image)'
    )

    args = parser.parse_args()

    if not args.quiet:
        print(f'Retrieving all images from {args.input_folder}')

    grouped_images = get_grouped_images(args.input_folder)

    if not grouped_images:
        print(f'No images were found in {args.input_folder}, nothing to do')
        sys.exit(1)

    if args.output_folder is not None:
        if os.path.exists(args.output_folder):
            print(f'{args.output_folder} already exists')
            sys.exit(2)

        output_folder = args.output_folder
    else:
        for idx in range(100):
            output_folder = f'lomosplit_output_{idx}'

            if not os.path.exists(output_folder):
                break
        else:
            print('Can\'t find appropriate name for output folder, please specify it')
            sys.exit(3)

    if args.frame_format not in ('jpg', 'jpeg', 'png'):
        print('Frame format must be jpg, jpeg or png')
        sys.exit(3)

    frame_template = f'{args.frame_template}.{args.frame_format}'

    for path, files in grouped_images:
        os.makedirs(os.path.join(output_folder, path), exist_ok=True)

        if not args.quiet:
            print(f'Processing {path}')

        for frame, frame_idx in enumerate(process_batch(
            files,
            luminosity_percentile=args.luminosity_percentile,
            rotate_image=args.rotate_image,
            rotate_frame=args.rotate_frame,
            frame_min_height=args.frame_min_height,
            frame_max_height=args.frame_max_height,
            adjust_to_max_height=args.adjust_to_max_height
        )):
            frame_filename = frame_template.format(
                idx=frame_idx
            )

            if not args.quiet:
                print(f'Saving {frame_filename}')

            skimage.io.imsave(
                os.path.join(
                    output_folder,
                    path,
                    frame_filename
                ),
                frame
            )

    if not args.quiet:
        print()
        print('Done')


if __name__ == '__main__':
    main()
