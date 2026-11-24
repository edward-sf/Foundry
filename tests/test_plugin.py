import json
import unittest

from contract import AGENT_MODELS, ROOT, SKILLS, read_frontmatter


class PluginManifest(unittest.TestCase):
    def test_manifest_name(self):
        manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        self.assertEqual(manifest["name"], "foundry")
        self.assertTrue(manifest.get("version"))
        self.assertTrue(manifest.get("description"))

    def test_agent_models(self):
        for name, model in AGENT_MODELS.items():
            with self.subTest(agent=name):
                fm = read_frontmatter(f"agents/{name}.md")
                self.assertEqual(fm.get("name"), name)
                self.assertEqual(fm.get("model"), model)
                self.assertTrue(fm.get("description"))

    @unittest.expectedFailure
    def test_skill_frontmatter(self):
        for skill in SKILLS:
            with self.subTest(skill=skill):
                fm = read_frontmatter(f"skills/{skill}/SKILL.md")
                self.assertEqual(fm.get("name"), skill)
                self.assertTrue(fm.get("description"))


if __name__ == "__main__":
    unittest.main()
