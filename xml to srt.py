import os
import xml.etree.ElementTree as ET

def ttml_to_srt_folder(input_folder, output_folder):
    # Namespace do TTML
    namespace = {
        'ttml': 'http://www.w3.org/ns/ttml',
        'tts': 'http://www.w3.org/ns/ttml#styling'
    }

    # Verificar se a pasta de saída existe; se não, criá-la
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Listar todos os arquivos na pasta de entrada
    files_converted = 0
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.xml') or filename.lower().endswith('.ttml'):
            ttml_file = os.path.join(input_folder, filename)
            srt_filename = os.path.splitext(filename)[0] + '.srt'
            srt_file = os.path.join(output_folder, srt_filename)

            print(f"Convertendo '{filename}' para '{srt_filename}'...")

            try:
                tree = ET.parse(ttml_file)
                root = tree.getroot()

                # Mapear estilos do TTML para SRT
                styles = {}
                positions = {}

                # Processar estilos
                for style in root.findall('.//ttml:style', namespace):
                    style_id = style.attrib.get('{http://www.w3.org/XML/1998/namespace}id')
                    font_style = style.attrib.get('{http://www.w3.org/ns/ttml#styling}fontStyle')
                    if font_style == 'italic':
                        styles[style_id] = ('<i>', '</i>')
                    # Apenas o itálico está mapeado

                # Processar regiões (posicionamento)
                for region in root.findall('.//ttml:region', namespace):
                    region_id = region.attrib.get('{http://www.w3.org/XML/1998/namespace}id')
                    display_align = region.attrib.get('{http://www.w3.org/ns/ttml#styling}displayAlign')
                    if display_align == 'before':
                        positions[region_id] = '{\\an8}%s'  # Topo da tela

                with open(srt_file, 'w', encoding='utf-8') as srt:
                    index = 1
                    for p in root.findall('.//ttml:p', namespace):
                        begin = p.attrib.get('begin')
                        end = p.attrib.get('end')
                        region = p.attrib.get('region')
                        p_style = p.attrib.get('style')

                        # Converter tempo para SRT
                        def convert_time(t):
                            # Remover 't' no final e converter para segundos
                            t_in_sec = float(t.rstrip('t')) / 10000000
                            # Converter para horas, minutos, segundos e milissegundos
                            hours = int(t_in_sec // 3600)
                            minutes = int((t_in_sec % 3600) // 60)
                            seconds = int(t_in_sec % 60)
                            milliseconds = int((t_in_sec % 1) * 1000)
                            return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

                        start_time = convert_time(begin)
                        end_time = convert_time(end)

                        # Função para extrair texto incluindo quebras de linha e aplicar estilos
                        def get_text_with_breaks(elem, current_style=None):
                            texts = []

                            # Atualizar o estilo atual se o elemento tiver um estilo
                            elem_style = elem.attrib.get('style', current_style)

                            # Iniciar a tag de estilo se ela começar neste elemento
                            started_new_style = False
                            if elem_style != current_style and elem_style in styles:
                                start_tag, end_tag = styles[elem_style]
                                texts.append(start_tag)
                                started_new_style = True

                            # Adicionar texto
                            if elem.text:
                                texts.append(elem.text)

                            for child in elem:
                                if child.tag == '{http://www.w3.org/ns/ttml}br':
                                    texts.append('\n')
                                else:
                                    # Processar elementos filhos
                                    texts.append(get_text_with_breaks(child, elem_style))

                                # Adicionar tail (texto após o elemento filho)
                                if child.tail:
                                    texts.append(child.tail)

                            # Fechar a tag de estilo se ela foi iniciada neste elemento
                            if started_new_style:
                                texts.append(end_tag)

                            return ''.join(texts)

                        text = get_text_with_breaks(p).strip()

                        # Aplicar estilo ao parágrafo, se houver
                        if p_style in styles and p_style != '':
                            start_tag, end_tag = styles[p_style]
                            text = f"{start_tag}{text}{end_tag}"

                        # Aplicar posicionamento
                        if region in positions:
                            text = positions[region] % text

                        # Escrever no arquivo SRT
                        srt.write(f"{index}\n")
                        srt.write(f"{start_time} --> {end_time}\n")
                        srt.write(f"{text}\n\n")
                        index += 1

                files_converted += 1
                print(f"Arquivo '{srt_filename}' criado com sucesso.\n")

            except Exception as e:
                print(f"Erro ao converter '{filename}': {e}\n")

    print(f"Conversão concluída. {files_converted} arquivo(s) convertido(s).")

# Exemplo de uso:
input_folder = 'input'   # Substitua pelo caminho da pasta de entrada
output_folder = 'output'    # Substitua pelo caminho da pasta de saída

ttml_to_srt_folder(input_folder, output_folder)
