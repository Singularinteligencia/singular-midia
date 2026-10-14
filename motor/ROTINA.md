# Rotina de ajustes de arte do Instagram da Singular

Esta pasta é o motor de artes do Instagram @singularinteligencia. A rotina abaixo roda de hora em hora para refazer artes que o Robert pediu para ajustar pela Central de Operações.

## Onde estão as coisas

- **Central de Operações** (artefato do Claude): https://claude.ai/artifact/7Fb2aXNFS4JM1S8YYvdE8P
  - Banco do artefato, coleção `redes`. Cada post agendado tem um documento `post<uuid do Metricool>` com:
    - `thumbs` (imagens de prévia, urls `/_blob/...`), `video` (prévia do Reels), `titulo`
    - `ajustes`: lista de `{texto, status, em, resposta}`. Status: `pendente` (a página ainda está aplicando), `arte` (precisa refazer imagem ou vídeo), `feito`.
  - Documentos `part-*` com `tipo: participacao` são posts que dependem de vídeo ou foto da equipe (não mexer, só lembrar).
- **Metricool**: blogId/brandId `7426071`, fuso `America/Sao_Paulo`, rede `instagram`.
- **Mídia pública**: este repositório. As artes publicadas ficam em `posts/AAAA-MM-DD-nome/` e são usadas por link raw do GitHub (`https://raw.githubusercontent.com/Singularinteligencia/singular-midia/main/posts/...`). Repositório público: nunca colocar material de cliente.
- **Motor**: `motor/` (este diretório). Rode `bash motor/setup.sh` antes de usar; os scripts esperam ficar em `/home/claude`.
  - `brand.py`: padrão visual dos cards 4:5 (2160x2700): fundo escuro com gradiente e grão, laranja #FF5D02, Poppins, `capa_faixa` para capa com foto.
  - `reels_texto.py` + `reels_semana.py`: Reels 9:16 com texto animado e trilha (`musica_reels.py`). Cada Reels é uma lista de cenas em `reels_semana.py`.
  - `alerta_dctfweb.py`, `capa_alerta_foto.py`: carrossel do pilar Alerta da Operação.

## Regras de conteúdo (obrigatórias)

- Nunca citar a marca TOTVS, suas linhas ou produtos (restrição legal). Pode falar de ERP, folha, eSocial, reforma tributária, gestão de pessoas.
- Nunca usar travessão (—). Usar dois-pontos, vírgula, ponto e vírgula, parênteses ou ponto.
- Não citar nomes de clientes.
- Visual: sempre o padrão escuro com laranja de destaque. Fundo laranja cheio foi rejeitado. Vídeos coloridos (não P&B).

## Passo a passo de cada execução

1. Ler a coleção `redes` do artefato (ArtifactData, action `list`).
2. Separar os ajustes com `status: "arte"`. Se não houver nenhum, encerrar sem fazer nada e sem avisar ninguém.
3. Para cada ajuste:
   1. Buscar o post no Metricool (`getScheduledPosts` dos próximos 120 dias) pelo `uuid`. Se a data já passou, marcar o ajuste como `feito` com resposta "Post já publicado; ajuste não aplicado" e seguir.
   2. Clonar este repositório e rodar `bash motor/setup.sh`.
   3. Refazer a arte pedida com o motor:
      - Reels: editar a cena correspondente em `reels_semana.py` (ou criar uma função nova) e renderizar `python3 reels_semana.py <letra>`.
      - Cards: baixar os JPGs atuais de `posts/...` se for só trocar um card, ou recriar com `brand.py`.
   4. Conferir o resultado olhando quadros/cards (Read na imagem) antes de publicar.
   5. Salvar com nome novo (ex.: `reels_v2.mp4`, `2_lista_v2.jpg`) em `posts/<pasta do post>/`, fazer commit e push para `main`, e testar o link raw (HTTP 200).
   6. `updateScheduledPost` no Metricool com o post completo (mesmo texto, data, tipo, `isAiGenerated`, `videoCoverMilliseconds`), trocando só `media`. Se o post estava como rascunho por causa do ajuste (`draft: true` e o motivo começa com "Aguardando ajuste"), devolver `draft: false`.
   7. Gerar prévias pequenas (imagens 540x675; vídeo 540 de largura, crf 28) e subir no artefato (Artifact publish com `asset: true`, `url` da Central, arquivos no diretório de trabalho). Atualizar o documento `post<uuid>`: `thumbs`/`video` novos e o ajuste com `status: "feito"`, `feitoEm` e `resposta` (uma frase dizendo o que mudou).
4. Se algo der errado, marcar o ajuste com `status: "arte"` e `resposta` explicando o problema em uma frase, para aparecer na Central.
