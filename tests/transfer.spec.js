const { test, expect } = require('@playwright/test');

const url = '/?balance=30000&reserved=20001';

test.beforeEach(async ({ page }) => {
  await page.goto(url);
});

test('Комиссия округляется вниз', async ({ page }) => {
  await page.click('text=Рублёвый счёт');

  const cardInput = page.locator('input');
  await cardInput.fill('1111222233334444');

  const amountInput = page.locator('input[type="number"]');
  await amountInput.fill('99');

  await expect(page.locator('text=9')).toBeVisible();
});

test('Нельзя ввести более 16 цифр карты', async ({ page }) => {
  await page.click('text=Рублёвый счёт');

  const cardInput = page.locator('input');

  await cardInput.fill('11112222333344445');

  await expect(cardInput).toHaveValue('1111222233334444');
});

test('Нельзя вводить отрицательную сумму', async ({ page }) => {
  await page.click('text=Рублёвый счёт');

  const cardInput = page.locator('input');
  await cardInput.fill('1111222233334444');

  const amountInput = page.locator('input[type="number"]');
  await amountInput.fill('-100');

  await expect(amountInput).toHaveValue('');
});
