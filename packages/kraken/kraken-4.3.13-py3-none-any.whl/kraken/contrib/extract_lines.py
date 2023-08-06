#! /usr/bin/env python

import click


@click.command()
@click.option('-f', '--format-type', type=click.Choice(['xml', 'alto', 'page', 'binary']), default='xml',
              help='Sets the input document format. In ALTO and PageXML mode all '
              'data is extracted from xml files containing both baselines, polygons, and a '
              'link to source images.')
@click.option('-i', '--model', default=None, show_default=True, type=click.Path(exists=True),
              help='Baseline detection model to use. Overrides format type and expects image files as input.')
@click.option('--repolygonize/--no-repolygonize', show_default=True,
              default=False, help='Repolygonizes line data in ALTO/PageXML '
              'files. This ensures that the trained model is compatible with the '
              'segmenter in kraken even if the original image files either do '
              'not contain anything but transcriptions and baseline information '
              'or the polygon data was created using a different method. Will '
              'be ignored in `path` mode. Note, that this option will be slow '
              'and will not scale input images to the same size as the segmenter '
              'does.')
@click.argument('files', nargs=-1)
def cli(format_type, model, repolygonize, files):
    """
    A small script extracting rectified line polygons as defined in either ALTO or
    PageXML files or run a model to do the same.
    """
    if len(files) == 0:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit()

    from PIL import Image
    from os.path import splitext
    from kraken import blla
    from kraken.lib import segmentation, vgsl, xml
    import io
    import json
    import pyarrow as pa

    if model is None:
        for doc in files:
            click.echo(f'Processing {doc} ', nl=False)
            if format_type != 'binary':
                data = xml.preparse_xml_data([doc], format_type, repolygonize=repolygonize)
                if len(data) > 0:
                    bounds = {'type': 'baselines', 'lines': [{'boundary': t['boundary'], 'baseline': t['baseline'], 'text': t['text']} for t in data]}
                    for idx, (im, box) in enumerate(segmentation.extract_polygons(Image.open(data[0]['image']), bounds)):
                        click.echo('.', nl=False)
                        im.save('{}.{}.jpg'.format(splitext(data[0]['image'])[0], idx))
                        with open('{}.{}.gt.txt'.format(splitext(data[0]['image'])[0], idx), 'w') as fp:
                            fp.write(box['text'])
            else:
                with pa.memory_map(doc, 'rb') as source:
                    ds_table = pa.ipc.open_file(source).read_all()
                    raw_metadata = ds_table.schema.metadata
                    if not raw_metadata or b'lines' not in raw_metadata:
                        raise ValueError(f'{doc} does not contain a valid metadata record.')
                    metadata = json.loads(raw_metadata[b'lines'])
                    for idx in range(metadata['counts']['all']):
                        sample = ds_table.column('lines')[idx].as_py()
                        im = Image.open(io.BytesIO(sample['im']))
                        im.save('{}.{}.jpg'.format(splitext(doc)[0], idx))
                        with open('{}.{}.gt.txt'.format(splitext(doc)[0], idx), 'w') as fp:
                            fp.write(sample['text'])
    else:
        net = vgsl.TorchVGSLModel.load_model(model)
        for doc in files:
            click.echo(f'Processing {doc} ', nl=False)
            full_im = Image.open(doc)
            bounds = blla.segment(full_im, model=net)
            for idx, (im, box) in enumerate(segmentation.extract_polygons(full_im, bounds)):
                click.echo('.', nl=False)
                im.save('{}.{}.jpg'.format(splitext(doc)[0], idx))


if __name__ == '__main__':
    cli()
