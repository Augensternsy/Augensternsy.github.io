const { test, expect } = require('@playwright/test');

const BASE_URL = 'https://augensternsy.github.io/';

test.describe('诗颖面试助手功能测试', () => {
  test('网站应该能够正常加载', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // 验证页面标题
    await expect(page).toHaveTitle(/Augensternsy/);
    
    // 验证页面核心元素存在
    await expect(page.locator('#navContainer')).toBeVisible();
    await expect(page.locator('.brand-logo')).toBeVisible();
  });

  test('验证导航栏功能', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // 验证导航菜单项存在
    const navItems = ['首页', '标签', '分类', '归档', '关于', '留言板', '友情链接'];
    
    for (const item of navItems) {
      const navItem = page.locator('.nav-menu', { hasText: item });
      await expect(navItem).toBeVisible();
    }
  });

  test('验证页面响应式布局', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // 测试桌面端布局
    await page.setViewportSize({ width: 1280, height: 720 });
    await expect(page.locator('#navContainer')).toBeVisible();
    
    // 测试移动端布局
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator('.mobile-head')).toBeVisible();
  });

  test('验证轮播图功能', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // 验证轮播图容器存在
    await expect(page.locator('.carousel')).toBeVisible();
    
    // 验证轮播图项目存在
    await expect(page.locator('.carousel-item')).toBeVisible();
  });

  test('验证文章卡片显示', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // 向下滚动到文章区域
    await page.locator('#indexCard').scrollIntoViewIfNeeded();
    
    // 验证文章卡片存在
    const articleCards = page.locator('.article .card');
    await expect(articleCards.first()).toBeVisible();
  });

  test('验证页脚信息', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // 滚动到页脚
    await page.locator('.page-footer').scrollIntoViewIfNeeded();
    
    // 验证页脚内容
    await expect(page.locator('.copy-right')).toBeVisible();
    await expect(page.locator('.social-link')).toBeVisible();
  });

  test('验证搜索功能', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // 点击搜索图标
    await page.locator('#searchIcon').click();
    
    // 验证搜索模态框出现
    await expect(page.locator('#searchModal')).toBeVisible();
    
    // 验证搜索输入框存在
    await expect(page.locator('#searchInput')).toBeVisible();
  });

  test('验证外部链接可访问性', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // 验证 GitHub 链接
    const githubLink = page.locator('a[href*="github.com"]').first();
    await expect(githubLink).toBeVisible();
    
    // 验证 RSS 订阅链接
    const rssLink = page.locator('.social-link a[href*="atom.xml"]').first();
    await expect(rssLink).toBeVisible();
  });
});
