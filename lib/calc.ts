import { CalcType, TonBasis } from '@prisma/client';

type Num = number;
const n = (v: any) => Number(v ?? 0);

export function calculateTanker(input: any) {
  const tonnage = input.tonBasis === TonBasis.PRODUCT ? n(input.productWeight) : n(input.billWeight);
  const customerAfnCosts = n(input.mahsuli) + n(input.fawaed) + n(input.fm60) + n(input.fm20) + n(input.qualityControl) + n(input.dozbolaghCustomer) + n(input.freightAfnCustomer) + n(input.miscAfnCustomer);
  const customerUsdCosts = n(input.jawazCommissionCustomer) + n(input.freightUsdCustomer) + n(input.miscUsdCustomer);
  const supplierAfn = n(input.mahsuli) + n(input.fawaed) + n(input.fm60) + n(input.fm20) + n(input.qualityControl) + n(input.dozbolaghSupplier) + n(input.freightAfnSupplier) + n(input.miscAfnSupplier);
  const supplierUsd = n(input.jawazCommissionSupplier) + n(input.freightUsdSupplier) + n(input.miscUsdSupplier);

  let customerDebtAfnCalc = 0;
  let customerDebtUsdCalc = 0;

  if (input.calcType === CalcType.PER_TON) {
    customerDebtAfnCalc = tonnage * n(input.perTonAfn);
    customerDebtUsdCalc = tonnage * n(input.perTonUsd);
  } else if (input.calcType === CalcType.COST) {
    customerDebtAfnCalc = customerAfnCosts;
    customerDebtUsdCalc = customerUsdCosts;
  } else {
    const ex = n(input.exchangeRate);
    const usdFromAfn = ex > 0 ? customerAfnCosts / ex : 0;
    customerDebtUsdCalc = usdFromAfn + customerUsdCosts;
  }

  return {
    customerDebtAfnCalc,
    customerDebtUsdCalc,
    customerInKindCalc: n(input.customerInKindCalc),
    supplierRecvAfnCalc: supplierAfn,
    supplierRecvUsdCalc: supplierUsd
  };
}
