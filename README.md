Function:
This script take a vcf and a csv produced by rPinecone then outputs a suitable panel.json for mykrobe to use

Usage example:
python3 make_tp_panel.py \
  --vcf 2025-01-31_masked_snps.vcf \
  --csv rPineCone9-5.pinecone.bootstrap.table.csv \
  --bootstrap pinecone_50 \
  --output treponema_panel.json

Requirments:
PyVCF

