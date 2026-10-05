import os
import sys
from pathlib import Path

# Add backend directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veyra_core.settings')
import django
django.setup()

from apps.careers.models import Career, CompetencyArea, Skill, SkillPrerequisite, Topic, Resource

def run_seed():
    print("Seeding full curriculum for 4 professions...")

    # 1. Tech: Junior Fullstack Developer
    tech = Career.objects.get(slug='junior-fullstack-developer')
    c1, _ = CompetencyArea.objects.get_or_create(career=tech, title="Frontend Engineering", defaults={'sort_order': 1})
    c2, _ = CompetencyArea.objects.get_or_create(career=tech, title="Backend & API Design", defaults={'sort_order': 2})
    c3, _ = CompetencyArea.objects.get_or_create(career=tech, title="Database Architecture", defaults={'sort_order': 3})

    s_html, _ = Skill.objects.get_or_create(
        competency_area=c1, slug="html-accessibility",
        defaults={'title': "Semantic HTML & Accessibility", 'description': "Build semantic, WCAG-compliant web layouts.", 'taxonomy': "APPLY", 'estimated_hours': 6.0}
    )
    s_css, _ = Skill.objects.get_or_create(
        competency_area=c1, slug="css-responsive",
        defaults={'title': "Modern Responsive CSS", 'description': "Master Flexbox, CSS Grid, and mobile-first design.", 'taxonomy': "APPLY", 'estimated_hours': 8.0}
    )
    s_js, _ = Skill.objects.get_or_create(
        competency_area=c1, slug="javascript-async",
        defaults={'title': "JavaScript Async & DOM", 'description': "Fetch APIs, async/await, and event-driven browser interactions.", 'taxonomy': "APPLY", 'estimated_hours': 12.0}
    )
    s_api, _ = Skill.objects.get_or_create(
        competency_area=c2, slug="rest-api-design",
        defaults={'title': "RESTful API Principles", 'description': "HTTP methods, status codes, idempotency, and contract design.", 'taxonomy': "UNDERSTAND", 'estimated_hours': 6.0}
    )
    s_server, _ = Skill.objects.get_or_create(
        competency_area=c2, slug="server-controllers",
        defaults={'title': "Server Routing & Endpoints", 'description': "Build backend controllers, middleware, and request validation.", 'taxonomy': "APPLY", 'estimated_hours': 10.0}
    )
    s_db, _ = Skill.objects.get_or_create(
        competency_area=c3, slug="relational-sql",
        defaults={'title': "Relational Data Modeling & SQL", 'description': "Tables, foreign keys, normalization, and ACID queries.", 'taxonomy': "ANALYZE", 'estimated_hours': 8.0}
    )

    # Prereq links
    SkillPrerequisite.objects.get_or_create(skill=s_css, prerequisite_skill=s_html)
    SkillPrerequisite.objects.get_or_create(skill=s_js, prerequisite_skill=s_css)
    SkillPrerequisite.objects.get_or_create(skill=s_server, prerequisite_skill=s_api)
    SkillPrerequisite.objects.get_or_create(skill=s_server, prerequisite_skill=s_db)

    # Topic & Resources
    t_html, _ = Topic.objects.get_or_create(skill=s_html, title="Semantic Document Structure", defaults={'sort_order': 1})
    Resource.objects.get_or_create(
        topic=t_html, title="MDN: HTML Elements Reference",
        defaults={
            'url': "https://developer.mozilla.org/en-US/docs/Web/HTML/Element",
            'provider_name': "Mozilla Developer Network",
            'resource_type': "DOCUMENTATION",
            'estimated_minutes': 25,
            'is_completely_free': True,
            'verification_status': "PUBLISHED"
        }
    )

    # 2. Healthcare: Medical Billing & Coding
    health = Career.objects.get(slug='medical-billing-and-coding')
    h1, _ = CompetencyArea.objects.get_or_create(career=health, title="Medical Foundations & Compliance", defaults={'sort_order': 1})
    h2, _ = CompetencyArea.objects.get_or_create(career=health, title="Diagnostic & Procedural Coding", defaults={'sort_order': 2})
    h3, _ = CompetencyArea.objects.get_or_create(career=health, title="Claim Cycle Management", defaults={'sort_order': 3})

    s_term, _ = Skill.objects.get_or_create(
        competency_area=h1, slug="medical-terminology",
        defaults={'title': "Medical Terminology & Anatomy", 'description': "Prefixes, roots, suffixes, and major human organ systems.", 'taxonomy': "REMEMBER", 'estimated_hours': 10.0}
    )
    s_hipaa, _ = Skill.objects.get_or_create(
        competency_area=h1, slug="hipaa-compliance",
        defaults={'title': "HIPAA Privacy & Data Standards", 'description': "Protected Health Information (PHI) safeguards and compliance.", 'taxonomy': "UNDERSTAND", 'estimated_hours': 6.0}
    )
    s_icd, _ = Skill.objects.get_or_create(
        competency_area=h2, slug="icd-10-basics",
        defaults={'title': "ICD-10-CM Diagnosis Coding", 'description': "Locate and assign accurate diagnostic classification codes.", 'taxonomy': "APPLY", 'estimated_hours': 14.0}
    )
    s_cpt, _ = Skill.objects.get_or_create(
        competency_area=h2, slug="cpt-procedure-coding",
        defaults={'title': "CPT Procedure Coding & Modifiers", 'description': "Code outpatient clinical, surgical, and diagnostic procedures.", 'taxonomy': "APPLY", 'estimated_hours': 12.0}
    )
    s_claim, _ = Skill.objects.get_or_create(
        competency_area=h3, slug="cms-1500-claims",
        defaults={'title': "CMS-1500 Claim Preparation", 'description': "Assemble, audit, and troubleshoot electronic healthcare claims.", 'taxonomy': "APPLY", 'estimated_hours': 8.0}
    )

    SkillPrerequisite.objects.get_or_create(skill=s_icd, prerequisite_skill=s_term)
    SkillPrerequisite.objects.get_or_create(skill=s_cpt, prerequisite_skill=s_icd)
    SkillPrerequisite.objects.get_or_create(skill=s_claim, prerequisite_skill=s_cpt)
    SkillPrerequisite.objects.get_or_create(skill=s_claim, prerequisite_skill=s_hipaa)

    t_icd, _ = Topic.objects.get_or_create(skill=s_icd, title="ICD-10-CM Coding Guidelines", defaults={'sort_order': 1})
    Resource.objects.get_or_create(
        topic=t_icd, title="CDC: Official ICD-10-CM Guidelines for Coding and Reporting",
        defaults={
            'url': "https://www.cdc.gov/nchs/icd/Comprehensive-Guidelines.htm",
            'provider_name': "Centers for Disease Control and Prevention",
            'resource_type': "DOCUMENTATION",
            'estimated_minutes': 35,
            'is_completely_free': True,
            'verification_status': "PUBLISHED"
        }
    )

    # 3. Finance: Staff Bookkeeper & Accountant
    fin = Career.objects.get(slug='staff-bookkeeper-accountant')
    f1, _ = CompetencyArea.objects.get_or_create(career=fin, title="Core Bookkeeping Foundations", defaults={'sort_order': 1})
    f2, _ = CompetencyArea.objects.get_or_create(career=fin, title="Cash & Ledger Management", defaults={'sort_order': 2})
    f3, _ = CompetencyArea.objects.get_or_create(career=fin, title="Financial Statement Synthesis", defaults={'sort_order': 3})

    s_double, _ = Skill.objects.get_or_create(
        competency_area=f1, slug="double-entry-accounting",
        defaults={'title': "Double-Entry Accounting & Debits/Credits", 'description': "Debit/credit duality, transaction analysis, and accounting equation.", 'taxonomy': "UNDERSTAND", 'estimated_hours': 8.0}
    )
    s_ledger, _ = Skill.objects.get_or_create(
        competency_area=f1, slug="chart-of-accounts-ledger",
        defaults={'title': "Chart of Accounts & General Ledger", 'description': "Post journal entries to general ledger and trial balances.", 'taxonomy': "APPLY", 'estimated_hours': 10.0}
    )
    s_recon, _ = Skill.objects.get_or_create(
        competency_area=f2, slug="bank-reconciliations",
        defaults={'title': "Bank & Credit Card Reconciliations", 'description': "Identify timing differences, deposits in transit, and bank fees.", 'taxonomy': "APPLY", 'estimated_hours': 8.0}
    )
    s_accruals, _ = Skill.objects.get_or_create(
        competency_area=f2, slug="accruals-adjusting-entries",
        defaults={'title': "Accruals & Period-End Adjusting Entries", 'description': "Prepaid expenses, depreciation, and accrued revenue adjustments.", 'taxonomy': "ANALYZE", 'estimated_hours': 10.0}
    )
    s_reports, _ = Skill.objects.get_or_create(
        competency_area=f3, slug="financial-statements",
        defaults={'title': "Balance Sheet & Income Statement Preparation", 'description': "Generate GAAP-compliant financial statements.", 'taxonomy': "CREATE", 'estimated_hours': 12.0}
    )

    SkillPrerequisite.objects.get_or_create(skill=s_ledger, prerequisite_skill=s_double)
    SkillPrerequisite.objects.get_or_create(skill=s_recon, prerequisite_skill=s_ledger)
    SkillPrerequisite.objects.get_or_create(skill=s_accruals, prerequisite_skill=s_ledger)
    SkillPrerequisite.objects.get_or_create(skill=s_reports, prerequisite_skill=s_accruals)
    SkillPrerequisite.objects.get_or_create(skill=s_reports, prerequisite_skill=s_recon)

    t_double, _ = Topic.objects.get_or_create(skill=s_double, title="The Accounting Equation & T-Accounts", defaults={'sort_order': 1})
    Resource.objects.get_or_create(
        topic=t_double, title="OpenStax: Principles of Financial Accounting Chapter 2",
        defaults={
            'url': "https://openstax.org/details/books/principles-financial-accounting",
            'provider_name': "OpenStax Rice University",
            'resource_type': "BOOK",
            'estimated_minutes': 45,
            'is_completely_free': True,
            'verification_status': "PUBLISHED"
        }
    )

    # 4. Skilled Trades: Residential Electrician Foundations
    elec = Career.objects.get(slug='residential-electrician-foundations')
    e1, _ = CompetencyArea.objects.get_or_create(career=elec, title="Electrical Physics & Safety", defaults={'sort_order': 1})
    e2, _ = CompetencyArea.objects.get_or_create(career=elec, title="Code Standards & Schematics", defaults={'sort_order': 2})
    e3, _ = CompetencyArea.objects.get_or_create(career=elec, title="Circuit Wiring Installation", defaults={'sort_order': 3})

    s_ohms, _ = Skill.objects.get_or_create(
        competency_area=e1, slug="ohms-law-power",
        defaults={'title': "Ohm's Law & Power Calculations", 'description': "Calculate voltage, current, resistance, and wattage in series/parallel circuits.", 'taxonomy': "APPLY", 'estimated_hours': 8.0}
    )
    s_osha, _ = Skill.objects.get_or_create(
        competency_area=e1, slug="osha-electrical-safety",
        defaults={'title': "OSHA Electrical Safety Standards", 'description': "Lockout/tagout (LOTO), arc flash risks, PPE, and personal safety.", 'taxonomy': "UNDERSTAND", 'estimated_hours': 6.0}
    )
    s_nec, _ = Skill.objects.get_or_create(
        competency_area=e2, slug="nec-navigation-standards",
        defaults={'title': "National Electrical Code (NEC) Navigation", 'description': "Look up code requirements for conductor ampacity and box sizing.", 'taxonomy': "APPLY", 'estimated_hours': 12.0}
    )
    s_circuits, _ = Skill.objects.get_or_create(
        competency_area=e3, slug="branch-circuit-wiring",
        defaults={'title': "Branch Circuit Wiring & Breaker Sizing", 'description': "Wire 120V receptacles, switches, and 15A/20A breaker panels.", 'taxonomy': "APPLY", 'estimated_hours': 10.0}
    )
    s_gfci, _ = Skill.objects.get_or_create(
        competency_area=e3, slug="gfci-three-way-circuits",
        defaults={'title': "GFCI, AFCI & Three-Way Switching", 'description': "Install ground-fault and arc-fault protection in wet and living areas.", 'taxonomy': "CREATE", 'estimated_hours': 12.0}
    )

    SkillPrerequisite.objects.get_or_create(skill=s_nec, prerequisite_skill=s_osha)
    SkillPrerequisite.objects.get_or_create(skill=s_circuits, prerequisite_skill=s_ohms)
    SkillPrerequisite.objects.get_or_create(skill=s_circuits, prerequisite_skill=s_nec)
    SkillPrerequisite.objects.get_or_create(skill=s_gfci, prerequisite_skill=s_circuits)

    t_ohms, _ = Topic.objects.get_or_create(skill=s_ohms, title="Ohm's Law Triangle & Equations", defaults={'sort_order': 1})
    Resource.objects.get_or_create(
        topic=t_ohms, title="All About Circuits: Ohm's Law and Power",
        defaults={
            'url': "https://www.allaboutcircuits.com/textbook/direct-current/chpt-2/voltage-current-resistance-relate/",
            'provider_name': "All About Circuits Textbook",
            'resource_type': "ARTICLE",
            'estimated_minutes': 25,
            'is_completely_free': True,
            'verification_status': "PUBLISHED"
        }
    )

    print("Curriculum successfully seeded!")

if __name__ == '__main__':
    run_seed()
