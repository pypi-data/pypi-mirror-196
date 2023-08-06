class MerCardInfo(object):
    """
    卡信息
    """
    card_type = ""
    card_name = ""
    card_no = ""
    prov_id = ""
    area_id = ""
    bank_code = ""
    branch_code = ""
    branch_name = ""
    cert_type = ""
    cert_no = ""
    cert_validity_type = ""
    cert_begin_date = ""
    cert_end_date = ""
    mp = ""

    def obj_to_dict(self):
        return {
            "card_type": self.card_type,
            "card_name": self.card_name,
            "card_no": self.card_no,
            "prov_id": self.prov_id,
            "area_id": self.area_id,
            "bank_code": self.bank_code,
            "branch_code": self.branch_code,
            "branch_name": self.branch_name,
            "cert_type": self.cert_type,
            "cert_no": self.cert_no,
            "cert_validity_type": self.cert_validity_type,
            "cert_begin_date": self.cert_begin_date,
            "cert_end_date": self.cert_end_date,
            "mp": self.mp
        }
