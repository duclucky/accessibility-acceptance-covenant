# { "Depends": "py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng" }

import genlayer as gl


class MinimalContract(gl.contract.Contract):
    value: str

    def __init__(self):
        self.value = "ok"

    @gl.public.view
    def get_value(self) -> str:
        return self.value
