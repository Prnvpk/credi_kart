document.addEventListener('DOMContentLoaded', () => {
  document.body.classList.add('is-loaded');

  const registerForm = document.querySelector('[data-register-form]');
  if (registerForm) {
    const role = registerForm.querySelector('[name="role"]');
    const shopkeeperFields = registerForm.querySelectorAll('[data-shopkeeper-field]');

    const syncShopkeeperFields = () => {
      const show = role && role.value === 'shopkeeper';
      shopkeeperFields.forEach((field) => {
        field.hidden = !show;
        field.querySelectorAll('input, select, textarea').forEach((input) => {
          input.disabled = !show;
        });
      });
    };

    if (role) {
      role.addEventListener('change', syncShopkeeperFields);
      syncShopkeeperFields();
    }
  }

  document.querySelectorAll('[data-quantity-control]').forEach((control) => {
    const value = control.querySelector('span');
    const buttons = control.querySelectorAll('button');
    const card = control.closest('.product-card');
    const addLink = card ? card.querySelector('.btn-add') : null;

    const syncHref = () => {
      if (!addLink) return;
      const url = new URL(addLink.href, window.location.origin);
      url.searchParams.set('quantity', value.textContent);
      addLink.href = url.toString();
    };

    buttons.forEach((button, index) => {
      button.addEventListener('click', () => {
        const current = Number.parseInt(value.textContent, 10) || 1;
        const next = index === 0 ? Math.max(1, current - 1) : Math.min(20, current + 1);
        value.textContent = next;
        syncHref();
      });
    });

    syncHref();
  });

  const chart = document.getElementById('adminChart');
  if (chart && window.Chart) {
    new Chart(chart, {
      type: 'bar',
      data: {
        labels: ['Sales', 'Credit', 'Repayments'],
        datasets: [{ data: [65, 42, 51], backgroundColor: ['#0f766e', '#c08400', '#2563eb'] }]
      },
      options: { plugins: { legend: { display: false } }, scales: { y: { display: false }, x: { grid: { display: false } } } }
    });
  }
});
