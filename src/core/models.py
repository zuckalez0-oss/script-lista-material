from dataclasses import dataclass


@dataclass(slots=True)
class MaterialItem:
    descricao: str
    aco: str
    comprimento_m: float
    peso_total: float
    codigo_excel: str
    tipo_perfil: str
    chave_agrupamento: str
    nome_normalizado: str


@dataclass(slots=True)
class MaterialGroup:
    descricao: str
    aco: str
    comprimento_m: float
    peso_total: float
    codigo_excel: str
    tipo_perfil: str
    chave_agrupamento: str
    nome_normalizado: str
    ocorrencias: int = 1

    @classmethod
    def from_item(cls, item: MaterialItem) -> "MaterialGroup":
        return cls(
            descricao=item.descricao,
            aco=item.aco,
            comprimento_m=item.comprimento_m,
            peso_total=item.peso_total,
            codigo_excel=item.codigo_excel,
            tipo_perfil=item.tipo_perfil,
            chave_agrupamento=item.chave_agrupamento,
            nome_normalizado=item.nome_normalizado,
            ocorrencias=1,
        )

    def merge(self, item: MaterialItem) -> None:
        self.comprimento_m += item.comprimento_m
        self.peso_total += item.peso_total
        self.ocorrencias += 1
