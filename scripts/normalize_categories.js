const fs = require('fs');
const path = require('path');

const POSTS_DIR = path.join(__dirname, '..', 'source', '_posts');

// Mapping from existing category labels to standardized 3-level path
// Each value is [level1, level2, level3]
const map = new Map([
  // Learning & Industry Trends
  ['前端开发', ['技术学习与行业趋势 / Learning & Industry Trends', '开发与技术栈 / Development & Tech Stack', '前端开发 / Frontend Development']],
  ['状态管理', ['技术学习与行业趋势 / Learning & Industry Trends', '开发与技术栈 / Development & Tech Stack', '状态管理 / State Management']],
  ['后端开发', ['技术学习与行业趋势 / Learning & Industry Trends', '开发与技术栈 / Development & Tech Stack', '后端开发 / Backend Development']],
  ['安全认证', ['技术学习与行业趋势 / Learning & Industry Trends', '开发与技术栈 / Development & Tech Stack', '安全认证 / Security Authentication']],
  ['API设计', ['技术学习与行业趋势 / Learning & Industry Trends', '开发与技术栈 / Development & Tech Stack', 'API设计 / API Design']],
  ['会话管理', ['技术学习与行业趋势 / Learning & Industry Trends', '开发与技术栈 / Development & Tech Stack', '会话管理 / Session Management']],
  ['开发工具', ['技术学习与行业趋势 / Learning & Industry Trends', '学习与工具 / Learning & Tools', '开发工具 / Development Tools']],
  ['版本控制', ['技术学习与行业趋势 / Learning & Industry Trends', '学习与工具 / Learning & Tools', '版本控制 / Version Control']],
  ['博客搭建', ['技术学习与行业趋势 / Learning & Industry Trends', '学习与工具 / Learning & Tools', '博客搭建 / Blog Setup']],
  ['编程规范', ['技术学习与行业趋势 / Learning & Industry Trends', '学习与工具 / Learning & Tools', '编程规范 / Coding Standards']],
  ['代码规范', ['技术学习与行业趋势 / Learning & Industry Trends', '学习与工具 / Learning & Tools', '代码规范 / Code Guidelines']],
  ['软件使用', ['技术学习与行业趋势 / Learning & Industry Trends', '学习与工具 / Learning & Tools', '软件使用 / Software Usage']],
  ['前端实践', ['技术学习与行业趋势 / Learning & Industry Trends', '开发与技术栈 / Development & Tech Stack', '前端实践 / Frontend Practices']],
  ['测试技术', ['测试基础与理论 / Testing Fundamentals', '测试理念与方法 / Testing Concepts & Methods', '测试方法 / Testing Methods']],
  ['测试基础', ['测试基础与理论 / Testing Fundamentals', '测试理念与方法 / Testing Concepts & Methods', '测试基础 / Testing Basics']],

  // Automation & Tools
  ['平台开发', ['自动化测试与工具开发 / Test Automation & Tool Development', '工具与平台开发 / Tools & Platform Development', '平台开发 / Platform Development']],
  ['测试平台', ['自动化测试与工具开发 / Test Automation & Tool Development', '工具与平台开发 / Tools & Platform Development', '平台开发 / Platform Development']],
  ['测试工具开发', ['自动化测试与工具开发 / Test Automation & Tool Development', '工具与平台开发 / Tools & Platform Development', '测试工具开发 / Test Tool Development']],
  ['测试框架', ['自动化测试与工具开发 / Test Automation & Tool Development', '自动化测试体系 / Automation Testing System', '测试框架设计 / Test Framework Design']],
  ['自动化测试', ['自动化测试与工具开发 / Test Automation & Tool Development', '自动化测试体系 / Automation Testing System', '自动化测试 / Automation Testing']],
  ['自动化工具', ['自动化测试与工具开发 / Test Automation & Tool Development', '工具与平台开发 / Tools & Platform Development', '自动化工具 / Automation Tools']],
  ['技术选型', ['自动化测试与工具开发 / Test Automation & Tool Development', '智能化与创新方向 / Intelligence & Innovation', '技术选型与架构设计 / Tech Selection & Architecture']],
  ['数据库维护', ['自动化测试与工具开发 / Test Automation & Tool Development', '工具与平台开发 / Tools & Platform Development', '数据库设计与维护 / Database Design & Maintenance']],

  // Performance & Security & Special Testing
  ['性能测试', ['性能、安全与专项测试 / Performance, Security & Special Testing', '性能类测试 / Performance Testing', '性能测试 / Performance Testing']],
  ['接口压测', ['性能、安全与专项测试 / Performance, Security & Special Testing', '性能类测试 / Performance Testing', '接口压测 / API Stress Testing']],

  // Project Practices & Case Studies
  ['项目实战', ['项目实战与案例经验 / Testing Practices & Case Studies', '项目实战 / Project Practices', '项目实战案例 / Project Case Studies']],
  ['数据驱动测试', ['项目实战与案例经验 / Testing Practices & Case Studies', '项目实战 / Project Practices', '数据驱动测试 / Data-driven Testing']],
  ['系统设计', ['项目实战与案例经验 / Testing Practices & Case Studies', '项目实战 / Project Practices', '系统设计 / System Design']],
  ['前后端分离', ['项目实战与案例经验 / Testing Practices & Case Studies', '项目实战 / Project Practices', '前后端分离 / Frontend-Backend Separation']],
  ['错误处理', ['项目实战与案例经验 / Testing Practices & Case Studies', '问题与解决 / Issues & Solutions', '错误处理与问题排查 / Error Handling & Troubleshooting']],
  ['问题排查', ['项目实战与案例经验 / Testing Practices & Case Studies', '问题与解决 / Issues & Solutions', '错误处理与问题排查 / Error Handling & Troubleshooting']],
  ['日志查询', ['项目实战与案例经验 / Testing Practices & Case Studies', '问题与解决 / Issues & Solutions', '日志分析与查询 / Log Analysis & Query']],
  ['日志分析', ['项目实战与案例经验 / Testing Practices & Case Studies', '问题与解决 / Issues & Solutions', '日志分析与查询 / Log Analysis & Query']],
  ['测试实践', ['项目实战与案例经验 / Testing Practices & Case Studies', '测试经验与落地 / Testing Experience', '测试实践总结 / Testing Practice Summary']],
  ['测试度量', ['测试基础与理论 / Testing Fundamentals', '质量度量与改进 / Quality Metrics & Improvement', '测试度量 / Test Metrics']],
  ['质量管理', ['测试基础与理论 / Testing Fundamentals', '质量度量与改进 / Quality Metrics & Improvement', '质量管理 / Quality Management']],
  ['Bug分析', ['项目实战与案例经验 / Testing Practices & Case Studies', '问题与解决 / Issues & Solutions', 'Bug分析 / Bug Analysis']],
  ['Bug管理', ['项目实战与案例经验 / Testing Practices & Case Studies', '问题与解决 / Issues & Solutions', 'Bug管理 / Bug Management']],

  // Certification & Training -> map to Testing Fundamentals / Knowledge
  ['认证学习 & 培训（Certification & Training）', ['测试基础与理论 / Testing Fundamentals', '测试知识沉淀 / Testing Knowledge', '测试培训笔记 / Training Notes']],
  ['SACA课程', ['测试基础与理论 / Testing Fundamentals', '测试知识沉淀 / Testing Knowledge', '测试培训笔记 / Training Notes']],
  ['数据分析', ['测试基础与理论 / Testing Fundamentals', '测试知识沉淀 / Testing Knowledge', '测试培训笔记 / Training Notes']],

  // Career & Thoughts
  ['博客介绍', ['职业成长与思考 / Career & Thoughts', '生活与思考 / Life & Thoughts', '博客介绍 / Blog Introduction']],
  ['职场经验', ['职业成长与思考 / Career & Thoughts', '个人成长 / Personal Growth', '求职与职场经验 / Job & Workplace Experience']],
  ['职业规划', ['职业成长与思考 / Career & Thoughts', '个人成长 / Personal Growth', '职业规划 / Career Planning']],
  ['学习方法', ['职业成长与思考 / Career & Thoughts', '个人成长 / Personal Growth', '学习方法 / Learning Methods']],
  ['代理服务器', ['职业成长与思考 / Career & Thoughts', '生活与思考 / Life & Thoughts', '代理服务器 / Proxy Server']],
  ['TUN模式', ['职业成长与思考 / Career & Thoughts', '生活与思考 / Life & Thoughts', 'TUN模式 / TUN Mode']],
  ['随笔类内容', ['职业成长与思考 / Career & Thoughts', '生活与思考 / Life & Thoughts', '随笔类内容 / Random Thoughts']],

  // AI & Research branch for new AI posts
  ['AI 框架', ['技术学习与行业趋势 / Learning & Industry Trends', 'AI与研究 / AI & Research', 'AI 框架与应用 / AI Frameworks & Applications']],
  ['研究实践', ['技术学习与行业趋势 / Learning & Industry Trends', 'AI与研究 / AI & Research', '研究实践 / Research Practices']],
  ['研究解读', ['技术学习与行业趋势 / Learning & Industry Trends', 'AI与研究 / AI & Research', '研究解读 / Research Analysis']],
  ['提示工程', ['技术学习与行业趋势 / Learning & Industry Trends', 'AI与研究 / AI & Research', '提示工程 / Prompt Engineering']],
  ['AI 框架与应用', ['技术学习与行业趋势 / Learning & Industry Trends', 'AI与研究 / AI & Research', 'AI 框架与应用 / AI Frameworks & Applications']],
]);

function extractFrontMatter(content) {
  const start = content.indexOf('---');
  if (start !== 0) return null;
  const end = content.indexOf('\n---', start + 3);
  if (end === -1) return null;
  const fm = content.slice(0, end + 4); // include trailing --- with newline
  const body = content.slice(end + 4);
  return { fm, body };
}

function getCategoriesFromFM(fm) {
  const m = fm.match(/\ncategories:\n([\s\S]*?)(\n[A-Za-z_]+:|\n---)/);
  if (!m) return null;
  const block = m[1];
  const lines = block.split('\n')
    .map(l => l.trim())
    .filter(l => l.startsWith('- '))
    .map(l => l.replace(/^-\s*/, ''));
  return { block, lines };
}

function replaceCategoriesInFM(fm, newCats) {
  const newBlock = 'categories:\n' + newCats.map(c => `  - ${c}`).join('\n');
  return fm.replace(/categories:\n([\s\S]*?)(\n[A-Za-z_]+:|\n---)/, (_, _block, tail) => newBlock + tail);
}

function normalizeLabel(label) {
  // Strip bilingual part after ' / ' and Chinese full-width parentheses '（...）'
  let base = label.split(' / ')[0];
  const parenIdx = base.indexOf('（');
  if (parenIdx !== -1) base = base.slice(0, parenIdx);
  return base.trim();
}

function getTagsKeywordsFromFM(fm) {
  const tagsMatch = fm.match(/\ntags:\n([\s\S]*?)(\n[A-Za-z_]+:|\n---)/);
  let tags = [];
  if (tagsMatch) {
    tags = tagsMatch[1]
      .split('\n')
      .map(t => t.trim())
      .filter(t => t.startsWith('- '))
      .map(t => t.replace(/^- +/, ''));
  }
  const kwMatch = fm.match(/\nkeywords:\s*(.+)\n/);
  let keywords = [];
  if (kwMatch) {
    keywords = kwMatch[1].split(',').map(s => s.trim().toLowerCase());
  }
  return { tags: tags.map(s => s.toLowerCase()), keywords };
}

function parseSlashCats(lines) {
  if (!lines.some(l => l.includes(' / '))) return null;
  const levels = lines.slice(0, 3);
  return {
    l1: levels[0] || '',
    l2: levels[1] || '',
    l3: levels[2] || ''
  };
}

function isAI(meta, name) {
  const needles = ['langchain','llm','agent','prompt','langgraph','langserve','langsmith','rag'];
  const pool = new Set([name, ...(meta.tags||[]), ...(meta.keywords||[])]);
  for (const n of needles) {
    for (const p of pool) {
      if (p && p.includes && p.includes(n)) return true;
    }
  }
  return false;
}

function decideNewCategories(lines, file, meta) {
  const name = path.basename(file).toLowerCase();
  const slashCats = parseSlashCats(lines);
  if (slashCats) {
    // Upgrade logic for already-standardized posts
    if (isAI(meta, name)) {
      // Promote to AI branch
      let l3 = 'AI 框架与应用 / AI Frameworks & Applications';
      const pool = new Set([name, ...(meta.tags||[]), ...(meta.keywords||[])]);
      if ([...pool].some(p => p.includes('prompt'))) {
        l3 = '提示工程 / Prompt Engineering';
      } else if ([...pool].some(p => p.includes('agent'))) {
        l3 = '代理与工作流 / Agents & Workflows';
      }
      const target = [
        '技术学习与行业趋势 / Learning & Industry Trends',
        'AI与研究 / AI & Research',
        l3
      ];
      const current = [slashCats.l1, slashCats.l2, slashCats.l3];
      // Only change if not already on target
      if (current[1] !== target[1] || current[2] !== target[2]) {
        return target;
      }
      return null;
    }
    // Non-AI posts: avoid generic "软件使用" where possible
    if (slashCats.l3 === '软件使用 / Software Usage') {
      if (name.includes('postman')) {
        return ['测试基础与理论 / Testing Fundamentals','测试理念与方法 / Testing Concepts & Methods','测试方法 / Testing Methods'];
      }
      if (name.includes('fiddler')) {
        return ['技术学习与行业趋势 / Learning & Industry Trends','学习与工具 / Learning & Tools','开发工具 / Development Tools'];
      }
      if (name.includes('version')) {
        return ['技术学习与行业趋势 / Learning & Industry Trends','学习与工具 / Learning & Tools','版本控制 / Version Control'];
      }
      if (name.includes('serialization')) {
        return ['技术学习与行业趋势 / Learning & Industry Trends','开发与技术栈 / Development & Tech Stack','后端开发 / Backend Development'];
      }
      if (name.includes('pinia')) {
        return ['技术学习与行业趋势 / Learning & Industry Trends','开发与技术栈 / Development & Tech Stack','状态管理 / State Management'];
      }
    }
    // Already standard and no upgrade needed
    return null;
  }

  // Not standardized yet: map by existing labels first
  for (const lRaw of lines) {
    const l = normalizeLabel(lRaw);
    if (map.has(l)) {
      return map.get(l);
    }
  }

  // Filename & tag heuristics
  if (isAI(meta, name)) {
    let l3 = 'AI 框架与应用 / AI Frameworks & Applications';
    const pool = new Set([name, ...(meta.tags||[]), ...(meta.keywords||[])]);
    if ([...pool].some(p => p.includes('prompt'))) {
      l3 = '提示工程 / Prompt Engineering';
    } else if ([...pool].some(p => p.includes('agent'))) {
      l3 = '代理与工作流 / Agents & Workflows';
    }
    return ['技术学习与行业趋势 / Learning & Industry Trends','AI与研究 / AI & Research', l3];
  }

  if (name.includes('pytest')) {
    return ['自动化测试与工具开发 / Test Automation & Tool Development', '自动化测试体系 / Automation Testing System', '测试框架设计 / Test Framework Design'];
  }
  if (name.includes('postman')) {
    return ['测试基础与理论 / Testing Fundamentals', '测试理念与方法 / Testing Concepts & Methods', '测试方法 / Testing Methods'];
  }
  if (name.includes('fiddler')) {
    return ['技术学习与行业趋势 / Learning & Industry Trends', '学习与工具 / Learning & Tools', '开发工具 / Development Tools'];
  }
  if (name.includes('log') && (name.includes('query') || name.includes('analysis'))) {
    return ['项目实战与案例经验 / Testing Practices & Case Studies', '问题与解决 / Issues & Solutions', '日志分析与查询 / Log Analysis & Query'];
  }
  if (name.includes('jmeter') || name.includes('performance')) {
    return ['性能、安全与专项测试 / Performance, Security & Special Testing', '性能类测试 / Performance Testing', '性能测试 / Performance Testing'];
  }
  if (name.includes('version') || name.includes('git')) {
    return ['技术学习与行业趋势 / Learning & Industry Trends', '学习与工具 / Learning & Tools', '版本控制 / Version Control'];
  }
  if (name.includes('serialization')) {
    return ['技术学习与行业趋势 / Learning & Industry Trends', '开发与技术栈 / Development & Tech Stack', '后端开发 / Backend Development'];
  }

  // Default fallback: Development Tools (avoid generic 软件使用)
  return ['技术学习与行业趋势 / Learning & Industry Trends', '学习与工具 / Learning & Tools', '开发工具 / Development Tools'];
}

function normalizeFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const parsed = extractFrontMatter(content);
  if (!parsed) return { changed: false, reason: 'no-front-matter' };
  const cats = getCategoriesFromFM(parsed.fm);
  if (!cats) return { changed: false, reason: 'no-categories' };
  const meta = getTagsKeywordsFromFM(parsed.fm);
  const newCats = decideNewCategories(cats.lines, filePath, meta);
  if (!newCats) {
    return { changed: false, reason: 'already-standard-or-no-change' };
  }
  const fmNew = replaceCategoriesInFM(parsed.fm, newCats);
  if (fmNew === parsed.fm) return { changed: false, reason: 'same' };
  const out = fmNew + parsed.body;
  fs.writeFileSync(filePath, out, 'utf8');
  return { changed: true, newCats };
}

function main() {
  const files = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));
  const results = [];
  for (const f of files) {
    const fp = path.join(POSTS_DIR, f);
    const res = normalizeFile(fp);
    results.push({ file: f, ...res });
  }
  // Write a summary file for review
  const summaryPath = path.join(__dirname, '..', 'source', '_data', 'category_normalize_summary.json');
  fs.writeFileSync(summaryPath, JSON.stringify(results, null, 2));
  console.log('Category normalization done. Summary at', summaryPath);
}

main();