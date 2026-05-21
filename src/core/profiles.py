import re

import docx

from src.core.models import MaterialItem
from src.utils import convert_to_mm


class MaterialProfileParser:
    def normalizar_nome_perfil_w(self, descricao: str) -> str:
        if not descricao:
            return ""

        match = re.search(r"W\s*(\d+)\s*[xX\s]*\s*([\d\.,]+)", descricao, re.IGNORECASE)
        if not match:
            return descricao.upper().strip()

        altura = match.group(1)
        peso = match.group(2).replace(".", ",")
        if peso.endswith(",0"):
            peso = peso[:-2]

        return f"W{altura}X{peso}"

    def classificar_e_mapear_perfil(self, descricao: str) -> tuple[str, str]:
        desc_upper = descricao.upper()

        if re.search(r"W\s*\d", desc_upper):
            return "VIGA W", "VIGA_W"

        if "[" in desc_upper or "][" in desc_upper:
            return "U.s", "PERFIL_U"
        if "UENR" in desc_upper or "IENR" in desc_upper or "CART" in desc_upper or "CA " in desc_upper:
            return "U.e", "TERCA"
        if "L DOBRADO" in desc_upper or desc_upper.startswith("L "):
            return "L DOBRADO", "CANTONEIRA"
        if "RED" in desc_upper:
            return "FERRO MECANICO RED.", "TUBO"
        if "TUBO" in desc_upper:
            return "TUBO", "TUBO"

        return "N/D", "OUTROS"

    def extrair_comprimento_texto(self, texto: str) -> float:
        regex_mm = r"(?:C|L|COMPR)[\s=:]*(\d{3,5})|(?:^|\s)(\d{3,5})\s*mm"
        match = re.search(regex_mm, texto, re.IGNORECASE)

        if not match:
            return 0.0

        valor_mm_str = match.group(1) if match.group(1) else match.group(2)
        try:
            return float(valor_mm_str) / 1000.0
        except ValueError:
            return 0.0

    def parse_dimensoes_inteligente(self, descricao: str, tipo_perfil: str) -> tuple[float, float, float, float]:
        a = b = c = esp = 0.0
        numeros_str_list = re.findall(r"[\d\./,]+", descricao)

        if tipo_perfil == "PERFIL_U":
            if len(numeros_str_list) >= 3:
                a = convert_to_mm(numeros_str_list[0])
                b = convert_to_mm(numeros_str_list[1])
                esp = convert_to_mm(numeros_str_list[2])
        elif tipo_perfil == "TERCA":
            if len(numeros_str_list) >= 4:
                a = convert_to_mm(numeros_str_list[0])
                b = convert_to_mm(numeros_str_list[1])
                c = convert_to_mm(numeros_str_list[2])
                esp = convert_to_mm(numeros_str_list[3])
        elif tipo_perfil == "CANTONEIRA":
            if len(numeros_str_list) >= 2:
                aba = convert_to_mm(numeros_str_list[0])
                a = aba
                b = aba
                esp = convert_to_mm(numeros_str_list[1])
        elif tipo_perfil == "TUBO" and len(numeros_str_list) >= 1:
            esp = convert_to_mm(numeros_str_list[0])

        return a, b, c, esp

    def gerar_chave_agrupamento(self, descricao: str, codigo_excel: str, tipo_perfil: str) -> str:
        if tipo_perfil == "VIGA_W":
            return f"VIGA_W::{self.normalizar_nome_perfil_w(descricao)}"

        descricao_limpa = descricao.upper()
        for termo in ("DUPLO", "DUPLA", "SIMPLES"):
            descricao_limpa = re.sub(rf"\b{termo}\b", "", descricao_limpa)
        descricao_limpa = re.sub(r"\s+", " ", descricao_limpa).strip()
        return f"{codigo_excel}::{descricao_limpa}"

    def criar_item(self, descricao: str, aco: str, comprimento_m: float, peso_total: float) -> MaterialItem:
        codigo_excel, tipo_perfil = self.classificar_e_mapear_perfil(descricao)
        nome_normalizado = self.normalizar_nome_perfil_w(descricao) if tipo_perfil == "VIGA_W" else descricao.upper().strip()
        chave_agrupamento = self.gerar_chave_agrupamento(descricao, codigo_excel, tipo_perfil)

        return MaterialItem(
            descricao=descricao,
            aco=aco,
            comprimento_m=comprimento_m,
            peso_total=peso_total,
            codigo_excel=codigo_excel,
            tipo_perfil=tipo_perfil,
            chave_agrupamento=chave_agrupamento,
            nome_normalizado=nome_normalizado,
        )
