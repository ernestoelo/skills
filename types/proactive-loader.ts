import z from "zod"
import { Skill } from "./skill"
import { Session } from "../session"
import { Log } from "../util/log"

export namespace ProactiveLoader {
  const log = Log.create({ service: "proactive-skill-loader" })

  const SKILL_PATTERNS: Record<string, RegExp[]> = {
    "architect": [
      /scaffold.*skill/i,
      /create.*skill/i,
      /skill.*template/i,
      /new.*skill/i
    ],
    "dev-workflow": [
      /git.*commit/i,
      /push.*pull/i,
      /merge.*branch/i,
      /version.*control/i
    ],
    "pdf": [
      /pdf.*process/i,
      /extract.*text.*pdf/i,
      /read.*pdf/i,
      /document.*processing/i
    ],
    "web-scraper": [
      /scrape.*web/i,
      /web.*crawler/i,
      /fetch.*url/i,
      /html.*markdown/i
    ],
    "sys-env": [
      /system.*environment/i,
      /arch.*linux/i,
      /hyprland/i,
      /package.*manager/i
    ],
    "code-review": [
      /code.*review/i,
      /security.*vulnerability/i,
      /code.*quality/i,
      /lint.*check/i
    ],
    "recursive-context": [
      /recursive.*context/i,
      /large.*input/i,
      /unlimited.*context/i,
      /chunk.*processing/i
    ],
    "mcp-builder": [
      /mcp.*server/i,
      /model.*context.*protocol/i,
      /external.*service/i,
      /api.*integration/i
    ]
  }

  export async function analyzeAndLoad(message: string): Promise<string[]> {
    const relevantSkills = analyzeMessage(message)

    if (relevantSkills.length > 0) {
      log.info("auto-activating skills", { skills: relevantSkills, message: message.slice(0, 100) })
      await loadSkills(relevantSkills)
    }

    return relevantSkills
  }

  function analyzeMessage(message: string): string[] {
    const activated: string[] = []

    for (const [skillName, patterns] of Object.entries(SKILL_PATTERNS)) {
      for (const pattern of patterns) {
        if (pattern.test(message)) {
          activated.push(skillName)
          break // Evitar duplicados
        }
      }
    }

    return activated
  }

  async function loadSkills(skillNames: string[]): Promise<void> {
    for (const name of skillNames) {
      const skill = await Skill.get(name)
      if (skill) {
        // Inyectar contenido del skill en el contexto de la sesión
        Session.injectSkill(skill)
        log.debug("skill loaded", { name })
      } else {
        log.warn("skill not found", { name })
      }
    }
  }
}