"""
Módulo do Motor de Inferência (Inference Engine)
Projeto: SE-RISK-TRADE (A1_LFA) - Sistema Especialista em Gestão de Risco Operacional na Bolsa de Valores
Autores: João Paulo de Oliveira Paiva e Danilo Hellu
Instituição: UDF Centro Universitário
Disciplina: Inteligência Artificial e LFA
Professora: Profa. Kadidja Valéria

Arquitetura e Comportamento:
1. Encadeamento para Frente (Forward Chaining): Processa fatos empíricos e preditivos em busca da conclusão resolutiva.
2. Resolução de Conflitos: Baseada em prioridade decrescente e especificidade lógica.
3. Tratamento de Incerteza ('?'): Preserva o valor ausente sem forçar inferências arriscadas, ativando disjuntores de segurança.
4. Módulo Explicativo: Implementa explicabilidade formal ('Como?' e 'Por quê?').
5. Trilha de Auditoria (Audit Trail): Registra o ciclo completo de avaliação das regras para conformidade regulatória CVM.
"""

from regras import REGRAS_RISCO_TRADE

class MotorInferenciaRisco:
    def __init__(self, regras=None):
        self.regras = sorted(
            regras or REGRAS_RISCO_TRADE,
            key=lambda r: r.get("prioridade", 0),
            reverse=True
        )
        self.memoria_trabalho = {}
        self.regras_disparadas = []
        self.rastro_execucao = []

    def carregar_fatos(self, fatos: dict):
        """Inicializa a memória de trabalho com os fatos da sessão."""
        self.memoria_trabalho = dict(fatos)
        self.regras_disparadas = []
        self.rastro_execucao = []

    def avaliar_condicoes(self, regra, fatos):
        """Verifica a correspondência lógica entre as condições da regra e os fatos."""
        if "condicoes_custom" in regra and callable(regra["condicoes_custom"]):
            return regra["condicoes_custom"](fatos)

        condicoes = regra.get("condicoes", {})
        if not condicoes:
            return True

        for chave, valor_esperado in condicoes.items():
            valor_fato = fatos.get(chave)
            if valor_fato != valor_esperado:
                return False
        return True

    def executar(self, fatos: dict):
        """
        Executa o ciclo de inferência por encadeamento para frente.
        Retorna o resultado determinístico com fundamentação legal e técnica.
        """
        self.carregar_fatos(fatos)
        regra_selecionada = None

        for regra in self.regras:
            id_regra = regra["id"]
            nome_regra = regra["nome"]
            satisfeita = self.avaliar_condicoes(regra, self.memoria_trabalho)

            registro = {
                "regra_id": id_regra,
                "regra_nome": nome_regra,
                "prioridade": regra.get("prioridade", 0),
                "satisfeita": satisfeita,
                "condicoes": regra.get("condicoes", {})
            }
            self.rastro_execucao.append(registro)

            if satisfeita:
                regra_selecionada = regra
                self.regras_disparadas.append(regra)
                # Resolução de conflito: a regra de maior prioridade aplicável determina a ação imediata
                break

        if not regra_selecionada:
            raise RuntimeError("Inconsistência crítica: nenhuma regra foi disparada na base de conhecimento.")

        explicacao_como = self.explicar_como(regra_selecionada)

        return {
            "acao_recomendada": regra_selecionada["acao"],
            "regra_id": regra_selecionada["id"],
            "regra_nome": regra_selecionada["nome"],
            "explicacao": regra_selecionada["explicacao"],
            "fundamento_legal": regra_selecionada.get("fundamento_legal", ""),
            "explicacao_como": explicacao_como,
            "fatos_utilizados": {
                k: self.memoria_trabalho[k]
                for k in regra_selecionada.get("condicoes", {}).keys()
                if k in self.memoria_trabalho
            },
            "total_regras_avaliadas": len(self.rastro_execucao)
        }

    def explicar_como(self, regra):
        """Gera a explicação detalhada de como os fatos acionaram a decisão."""
        condicoes = regra.get("condicoes", {})
        if not condicoes:
            return f"A regra [{regra['id']} - {regra['nome']}] foi aplicada como política residual de contingência (fallback)."

        termos = [f"{k} = '{v}'" for k, v in condicoes.items()]
        return (
            f"O sistema inferiu '{regra['acao']}' através da regra [{regra['id']} - {regra['nome']}], "
            f"pois foram validados os fatos: {', '.join(termos)}."
        )

    def explicar_por_que(self, id_regra):
        """Gera a fundamentação técnica e regulatória da existência da regra."""
        for r in self.regras:
            if r["id"] == id_regra:
                return (
                    f"Regra [{r['id']}] ({r['nome']}): {r['explicacao']} "
                    f"Fundamentação Regulatória: {r.get('fundamento_legal', 'Não especificada')}."
                )
        return f"Regra {id_regra} não encontrada no repositório."
