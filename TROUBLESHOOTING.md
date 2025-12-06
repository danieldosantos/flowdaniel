# Troubleshooting "mestre-galhart" Telegram flow

Use these checks when the flow para de responder mesmo com credenciais aparentemente corretas.

## 1) Confirmar que o workflow está ativo e recebendo webhooks
- No n8n, abra **mestre-galhart-workflow-centralizado** e verifique se o status está **Active**. Se estiver desativado o webhook do Telegram não fica registrado.
- Teste o endpoint do webhook exibido no nodo **Telegram Trigger** (webhookId `dc373f2f-7543-45c6-bd4a-55727264a116`) com um `curl` para garantir que o serviço responde (ex.: `curl -i <url-do-webhook>`).

## 2) Conferir permissões no Telegram
- Garanta que o bot não foi removido ou silenciado no grupo/supergrupo. Reinserir o bot costuma reativar permissões.
- Para grupos, confirme se o bot tem permissão de **Read messages** e **Send messages**.
- Se o bot estiver em modo de privacidade, adicione-o como admin ou desative a privacidade para receber todos os comandos.

## 3) Ver logs de erro no n8n
- No painel do n8n, abra **Executions** e procure falhas recentes. Erros em nós Gemini/PaLM, Redis ou Postgres impedem o fluxo de concluir a resposta.
- Clique numa execução falha para ver o nó exato que interrompeu o fluxo; isso revela se é limite de tokens, quota ou indisponibilidade externa.

## 4) Validar conectividade com serviços externos
- **Google Gemini/PaLM**: verifique limites de quota ou se o modelo configurado ainda está disponível. Ajustar o modelo ou reduzir a temperatura pode evitar bloqueios temporários.
- **Redis/Postgres**: confirme host/porta e autenticação. A ausência dessas dependências pode causar falha silenciosa antes da resposta chegar ao Telegram.

## 5) Testar com um comando simples
- Envie `/start` para o bot e confira se o JSON chega em `Executions` ou habilite temporariamente um nó **Debug** após o trigger para logar a mensagem.
- Se o trigger receber a mensagem mas nenhum texto for enviado de volta, foque nos nós de geração (Gemini) e envio (Telegram) da sequência correspondente.

## 6) Reimplantar o webhook quando trocar credenciais
- Mesmo que as credenciais estejam válidas, alterar o token do bot ou regenerar a URL pública exige reativar o workflow para registrar o novo webhook no Telegram.

Documentar o que aconteceu (mensagem, horário, nós com falha) ajuda a isolar a causa rapidamente caso o problema volte a ocorrer.

## 7) Interpretar a saída do Postgres PG Tool
- Quando o node retorna linhas como `0\nid:1\ntelegram_user_id:...`, significa que a consulta foi executada com sucesso e está exibindo a linha **0** do resultado (índice base 0). Os campos seguintes são as colunas da tabela.
- Para confirmar que não há erro de sintaxe, procure mensagens de erro destacadas em vermelho no painel "Output"; se não houver, a query está correta.
- Se precisar de mais linhas, ajuste a consulta para limitar ou ordenar conforme necessário (ex.: `ORDER BY created_at DESC LIMIT 5`).
- Caso espere colunas adicionais, confira se a tabela tem os campos certos com `SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'rpg_players';`.
