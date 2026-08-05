"""
Main Entry Point - Unlimited Autonomous AI Agent
=================================================

This is the main script to run the Unlimited Autonomous AI Agent.
For Vercel deployment, the entry point is api/index.py
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from src.core.unlimited_agent import UnlimitedAgent
    from src.core.memory import CoreMemory
    from src.tasks.task_manager import TaskManager
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("   Make sure all required files exist in src/")
    print("   If running on Vercel, this file is not used.")
    sys.exit(1)


def create_demo_tasks(agent: UnlimitedAgent) -> TaskManager:
    """Create demo tasks to test the agent"""
    task_manager = TaskManager(agent)
    
    demo_tasks = [
        {
            "description": "Analyze the current cryptocurrency market and identify trading opportunities",
            "priority": 5,
            "context": {'market': 'crypto', 'timeframe': '1h'},
            "deadline": "2024-12-31"
        },
        {
            "description": "Create a business plan for a new AI startup",
            "priority": 4,
            "context": {'industry': 'AI', 'phase': 'seed'},
            "deadline": "2024-12-15"
        },
        {
            "description": "Create a new bot that can analyze customer sentiment from social media",
            "priority": 3,
            "context": {'platform': 'twitter', 'language': 'all'},
            "deadline": "2025-01-15"
        },
        {
            "description": "Learn about quantum computing and its business applications",
            "priority": 2,
            "context": {'field': 'quantum', 'level': 'intermediate'},
            "deadline": "2025-02-01"
        }
    ]
    
    for task in demo_tasks:
        task_manager.add_task(**task)
    
    print(f"📋 Added {len(task_manager.tasks)} demo tasks")
    return task_manager


def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_menu():
    """Display main menu"""
    print("\n" + "="*70)
    print("WHAT WOULD YOU LIKE TO DO?")
    print("="*70)
    print("1. Process all pending tasks")
    print("2. Process one specific task")
    print("3. Add a new task")
    print("4. Create a new bot")
    print("5. Run autonomously")
    print("6. Show status")
    print("7. Show memory summary")
    print("8. Clear all tasks")
    print("9. Exit")
    print("-"*70)
    return input("Enter your choice (1-9): ").strip()


def main():
    """Main entry point"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🤖 UNLIMITED AUTONOMOUS AI AGENT                                          ║
║                                                                              ║
║   "The AI that can do ANY task, in ANY domain, ANYWHERE"                    ║
║                                                                              ║
║   Features:                                                                  ║
║   - Self-learning from books and experience                                ║
║   - Self-repairing when something breaks                                   ║
║   - Self-upgrading to become better                                         ║
║   - Self-replicating to create other bots                                  ║
║                                                                              ║
║   Domains: Business, Finance, Healthcare, Education, Technology, Legal,     ║
║             Creative, Real Estate, Manufacturing, Agriculture, Retail,       ║
║             Transportation, Energy, Government, and more...                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Initialize the agent
    print("\n" + "="*70)
    print("INITIALIZING AGENT...")
    print("="*70)
    
    try:
        agent = UnlimitedAgent()
        print("✅ Agent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return
    
    # Step 2: Add demo tasks
    print("\n" + "="*70)
    print("ADDING TASKS...")
    print("="*70)
    task_manager = create_demo_tasks(agent)
    
    # Step 3: Show initial status
    print("\n" + "="*70)
    print("INITIAL STATUS")
    print("="*70)
    try:
        status = agent.get_status()
        print(json.dumps(status, indent=2, default=str))
    except Exception as e:
        print(f"⚠️ Could not get status: {e}")
    
    # Step 4: Main loop
    while True:
        choice = show_menu()
        
        if choice == "1":
            # Process all tasks
            print("\n🔄 Processing all tasks...")
            pending = task_manager.get_pending_tasks()
            if not pending:
                print("✅ No pending tasks")
                continue
            
            for task in pending:
                try:
                    result = agent.process_task(task['description'], task.get('context'))
                    task_manager.mark_completed(task['id'], result)
                    status = "✅" if result.get('success') else "❌"
                    print(f"{status} Task {task['id']}: {task['description'][:50]}...")
                except Exception as e:
                    print(f"❌ Error processing task {task['id']}: {e}")
        
        elif choice == "2":
            # Process one specific task
            task_id = input("Enter task ID: ").strip()
            task = task_manager.get_task_by_id(task_id)
            if task:
                try:
                    result = agent.process_task(task['description'], task.get('context'))
                    task_manager.mark_completed(task['id'], result)
                    print(f"✅ Task completed: {result.get('success', False)}")
                except Exception as e:
                    print(f"❌ Error: {e}")
            else:
                print(f"❌ Task {task_id} not found")
        
        elif choice == "3":
            # Add a new task
            description = input("Enter task description: ").strip()
            if not description:
                print("❌ Description is required")
                continue
            
            context_input = input("Enter context (JSON format, or press Enter for empty): ").strip()
            try:
                context = json.loads(context_input) if context_input else {}
            except json.JSONDecodeError:
                print("❌ Invalid JSON format")
                continue
            
            priority_input = input("Enter priority (1-5, default 3): ").strip()
            priority = int(priority_input) if priority_input.isdigit() else 3
            
            task_id = task_manager.add_task(description, priority, context)
            print(f"✅ Task added with ID: {task_id}")
        
        elif choice == "4":
            # Create a new bot
            requirements = input("Enter bot requirements: ").strip()
            if not requirements:
                print("❌ Requirements are required")
                continue
            
            location = input("Enter location (local/cloud/remote): ").strip() or "local"
            
            try:
                from src.core.unlimited_agent import Task_CreateBot
                creator = Task_CreateBot(agent)
                result = creator.execute(requirements, location)
                if result.get('success'):
                    print(f"✅ Bot created at: {result.get('location', 'unknown')}")
                else:
                    print(f"❌ Bot creation failed: {result.get('message', 'Unknown error')}")
            except ImportError:
                print("❌ Bot creator not available")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == "5":
            # Run autonomously
            print("\n🤖 Starting autonomous mode...")
            print("   The agent will process tasks automatically")
            print("   Press Ctrl+C to stop")
            try:
                agent.run_autonomously()
            except KeyboardInterrupt:
                print("\n🛑 Stopped by user")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == "6":
            # Show status
            try:
                status = agent.get_status()
                print("\n" + "="*70)
                print("AGENT STATUS")
                print("="*70)
                print(json.dumps(status, indent=2, default=str))
            except Exception as e:
                print(f"❌ Error getting status: {e}")
        
        elif choice == "7":
            # Show memory summary
            try:
                memory = agent.memory.get_summary()
                print("\n" + "="*70)
                print("MEMORY SUMMARY")
                print("="*70)
                print(json.dumps(memory, indent=2, default=str))
            except Exception as e:
                print(f"❌ Error getting memory: {e}")
        
        elif choice == "8":
            # Clear all tasks
            confirm = input("⚠️ Are you sure you want to clear all tasks? (y/n): ").strip()
            if confirm.lower() == 'y':
                task_manager.tasks = []
                print("✅ All tasks cleared")
            else:
                print("❌ Cancelled")
        
        elif choice == "9":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-9.")
    
    # Show final status
    print("\n" + "="*70)
    print("FINAL STATUS")
    print("="*70)
    try:
        status = agent.get_status()
        print(json.dumps(status, indent=2, default=str))
    except:
        print("Could not get final status")
    
    print("\n✅ Agent execution complete!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
