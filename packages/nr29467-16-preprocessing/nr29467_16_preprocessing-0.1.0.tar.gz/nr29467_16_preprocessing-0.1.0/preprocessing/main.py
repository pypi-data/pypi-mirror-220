from pathlib import Path
import numpy as np
import click

from preprocessing.files import FileHandler, TiffHandler, H5Handler, get_handler
from preprocessing.clipping import clip_to_upper_hist, apply_clip_to_mask
import preprocessing.image_processing as ip

@click.command()
@click.argument('data_path', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path(exists=True), default=Path().absolute())
@click.option('-sd', '--sd_factor', default=1.5, help='How many standard deviations to clip')
@click.option('-ot', '--output-type', default='h5', help='Output file type, h5 or tiff')
@click.option('-r', '--rescale', is_flag=True, help='Rescale the data to [0, 1]', default=True)
def clip(data_path, output_dir, sd_factor, output_type, rescale):
    data_path = Path(data_path)
    output_dir = Path(output_dir)
    handle = get_handler(data_path, file=data_path)

    id_tag = f'{data_path.stem}_clipped'

    data = handle.read()
    lb, ub = clip_to_upper_hist(
        data.flatten(),
        output_dir,
        sd_factor=sd_factor,
        tag=id_tag,
    )
    data[data < lb] = lb
    data[data > ub] = ub

    print(f'min: {np.nanmin(data)}, max: {np.nanmax(data)}')
    print(f'rescale: {rescale}')
    if rescale:
        data = (data - np.nanmin(data)) / (np.nanmax(data) - np.nanmin(data))
        print(f'min: {np.nanmin(data)}, max: {np.nanmax(data)}')
    out_path = output_dir / f'{id_tag}.{output_type}'
    output_handler = get_handler(out_path)
    output_handler.write(
        out_path,
        data,
    )


@click.command()
@click.argument('data_path', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path(exists=True), default=Path().absolute())
@click.option('-s', '--sigma', default=1.5, help='Sigma value for Gaussian filter')
@click.option('-t', '--output-type', default='h5', help='Output file type, h5 or tiff')
def gaussian_blur(data_path, output_dir, sigma, output_type):
    data_path = Path(data_path)
    output_dir = Path(output_dir)
    handle = get_handler(data_path)(file=data_path)
    data = ip.denoise(
        handle.read(),
        output_dir,
        sigma=sigma,
    )
    out_path = output_dir / f'{data_path.stem}_denoised.{output_type}'
    output_handler = get_handler(out_path)
    output_handler.write(
        out_path,
        data,
    )

@click.group(
    help='Preprocessing pipeline for 3D image data',
)
def cli():
    pass

cli.add_command(clip)
cli.add_command(gaussian_blur)

if __name__ == '__main__':
    cli()